import ast
import os

from airflow.decorators import task
from airflow.models import DagModel
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
from utilities.ListLinkScraper import link_scrape
from airflow.utils.dates import days_ago
from airflow.models.variable import Variable
import pandas as pd
from utilities.ssh_tunnel import transmit_data_through_ssh_tunnel
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pylab

default_args = {
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
        dag_id="links",
        default_args=default_args,
        description='DAG to scrape 400 links (4*100) up to 5 times',
        # schedule_interval='0 */12 * * *',  # every 12 hours
        schedule_interval='*/10 * * * *',  # every 10 minutes
        catchup=False,
        max_active_runs=1,
) as links_dag:
    @task.branch(task_id="branch")
    def branch_func():
        times_ran = int(Variable.get("list_links_iterations", default_var=0))

        dag: DagModel = DagModel.get_dagmodel('etl_pipeline')
        if not dag.is_paused:
            return 'list_empty'

        # if times_ran < 5:
        if times_ran < 1:
            return 'link_scraping'
        else:
            # return 'handle_rescheduling'
            return 'placeholder_operator_before_stats'


    def profile_condition(row, select, over):
        """
        Function that returns rows with a selected profile over another profile
        Currently applicable only in the Style column, so it is related to genders

        Example -> If user wants to inspect Feminine perfumes,
        select='Feminine', over='Masculine'

        :param row: Current row in DataFrame
        :param select: Select this gender
        :param over: Ignore this gender
        :return:
        """
        profile = ast.literal_eval(row['style'])
        values = ast.literal_eval(row['style_numbers'])

        if select not in profile:
            return False

        if over not in profile:
            return True

        select_index = profile.index(select)
        over_index = profile.index(over)


        # If the style leans toward selected gender, return the row
        if values[select_index] > values[over_index]:
            return True
        else:
            return False


    def decade_info(decade: int | str = 'All'):
        try:
            pg_hook = PostgresHook(postgres_conn_id='dag_connection')
            connection = pg_hook.get_conn()

            df = None

            # if a specific decade is selected
            if decade != 'All':
                query = """SELECT * FROM etl_perfume 
                WHERE rel_decade = %s"""

                df = pd.read_sql_query(sql=query, params=[decade], con=connection)
            # otherwise, just get all the info
            else:
                query = "SELECT * FROM etl_perfume"
                df = pd.read_sql_query(sql=query, con=connection)

            # Get the directory where the current DAG file resides
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # define the folder and file path
            folder_name = 'temp'
            file_name = f'{decade}.csv'
            file_path = os.path.join(current_dir, folder_name, file_name)

            df.to_csv(file_path, index=False)
            print(f"DataFrame saved to: {file_path}")

        except Exception as e:
            print(e)
        finally:
            connection.close()


    def decade_gender_info(decade: int | str = 'All', gender: str = 'All'):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # define the folder and file path
            folder_name = 'temp'
            file_name = f'{decade}.csv'
            file_path = os.path.join(current_dir, folder_name, file_name)

            df = pd.read_csv(file_path)

            # TODO: Decide if I need to delete the csv files in temp

            df_filtered = None

            if gender == 'Masculine':
                df_filtered = df[df.apply(profile_condition, axis=1, args=('Masculine', 'Feminine'))]
            elif gender == 'Feminine':
                df_filtered = df[df.apply(profile_condition, axis=1, args=('Feminine', 'Masculine'))]
            else:
                df_filtered = df

            if df.empty:
                print("DataFrame is empty!")
                return

            df_filtered = df_filtered[['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']]

            # Calculate statistics
            summary = df_filtered.describe()
            median = df_filtered.median()
            # if multiple modes, select first one
            mode = df_filtered.mode().iloc[0]

            summary_transposed = summary.T  # Transpose summary statistics
            summary_transposed['median'] = median
            summary_transposed['mode'] = mode

            # Split the table into two parts
            columns_part1 = ['count', 'mean', 'median', 'mode', 'std']
            columns_part2 = ['25%', '50%', '75%', 'min', 'max', ]

            fig, axes = plt.subplots(2, 1, figsize=(5, 5))

            # First part of the table
            axes[0].axis('off')
            part1_table = axes[0].table(
                cellText=summary_transposed[columns_part1].round(2).values,
                rowLabels=summary_transposed.index,
                colLabels=columns_part1,
                loc='center'
            )

            # Second part of the table
            axes[1].axis('off')
            part2_table = axes[1].table(
                cellText=summary_transposed[columns_part2].round(2).values,
                rowLabels=summary_transposed.index,
                colLabels=columns_part2,
                loc='center'
            )

            # Adjust font size and layout
            for table in [part1_table, part2_table]:
                table.auto_set_font_size(False)
                table.set_fontsize(10)

            plt.tight_layout()

            file_name = f'{decade}_{gender}.png'
            file_path_save_table = os.path.join(current_dir, folder_name, file_name)

            # Save the figure
            plt.savefig(file_path_save_table, bbox_inches='tight')
            plt.close(fig)

            # Box Plot
            plt.figure(figsize=(8, 6))
            sns.boxplot(data=df_filtered)
            plt.title("Box Plots of Ratings")

            file_name = f'{decade}_{gender}_box_plots.png'
            file_path_box_plots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_box_plots, bbox_inches='tight')

            # QQ Plots
            fig, axes = plt.subplots(len(df_filtered.columns), 1, figsize=(6, 14))
            for i, col in enumerate(df_filtered.columns):
                print(df_filtered[col])
                stats.probplot(df_filtered[col], dist="norm", plot=axes[i])
                axes[i].set_title(f"QQ Plot for {col}")
                axes[i].set_xlabel("Ordered value quantiles")
                axes[i].set_xlabel("Normal quantiles")
            plt.tight_layout()

            file_name = f'{decade}_{gender}_qq_plots.png'
            file_path_qq_plots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_qq_plots, bbox_inches='tight')

            # Pairplot with histograms
            g = sns.pairplot(df_filtered, corner=True, diag_kind=None)

            # Replace diagonal elements with custom histograms
            for i in range(len(df_filtered.columns)):
                ax = g.axes[i, i]  # Access the diagonal subplot
                if ax is not None:  # Check if the axis exists
                    g.fig.delaxes(ax)  # Remove the existing axis
                    new_ax = g.fig.add_subplot(len(df_filtered.columns), len(df_filtered.columns),
                                               i * len(df_filtered.columns) + i + 1)  # Recreate axis

                    ax = sns.histplot(df_filtered.iloc[:, i], bins=15, kde=False, ax=new_ax,
                                      color="skyblue")  # Add histogram
                    ax.set_title(f"Histogram of {df_filtered.columns[i]}", fontsize=10, fontweight='bold')  # Add title

            g.fig.subplots_adjust(hspace=0.5, wspace=0.5)

            file_name = f'{decade}_{gender}_pairplots.png'
            file_path_pairplots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_pairplots, bbox_inches='tight')

            # Violin Plot
            plt.figure(figsize=(8, 6))
            sns.violinplot(data=df_filtered)
            plt.title("Violin Plots of Ratings")

            file_name = f'{decade}_{gender}_violin_plots.png'
            file_path_violin_plots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_violin_plots, bbox_inches='tight')


        except Exception as e:
            print(e)
        finally:
            return


    decade_operators = []
    decades = [1990, 2000, 2010, 2020, 'All']

    for decade in decades:
        decade_operators.append(
            PythonOperator(
                task_id=f"decade_task_{decade}",
                python_callable=decade_info,
                op_args=[decade],
            )
        )

    decade_gender_operators = [[], [], [], [], []]
    gender_profiles = ['Masculine', 'Feminine', 'All']

    for index, decade in enumerate(decades):
        for gender in gender_profiles:
            decade_gender_operators[index].append(
                PythonOperator(
                    task_id=f"decade_task_{decade}_gender_{gender}",
                    python_callable=decade_gender_info,
                    op_args=[decade, gender]
                )
            )


    def handle_rescheduling():
        # TRANSMIT DATA HERE, TRAIN MODELS HERE
        # if transmitting and training done, skip

        # TODO: Need to figure out a default return value
        time_etl_completion = datetime.strptime(Variable.get("time_etl_completion"), "%Y-%m-%d %H:%M:%S")
        # delta = timedelta(days=5) or (days=7)
        delta = timedelta(minutes=5)

        # TODO: What happens if you reschedule scraping while etl-pipeline is running?
        # This behaviour should be avoided, good weather does not allow it, but further testing needed
        # Possibly include dag.is_paused check in here
        if abs(time_etl_completion - datetime.now()) >= delta:
            print(f"Elapsed time between last total scrape job and now exceeds ${delta}. Scraping will resume soon...")
            Variable.set("list_links_iterations", 0)

            current_environment = os.getenv('PIPELINE', 'dev')

            if current_environment == 'production':
                transmit_data_through_ssh_tunnel()

            return
        else:
            print(f"Waiting time of ${delta} not reached. No actions will be taken until then...")
            return


    link_scraping_op = PythonOperator(
        task_id="link_scraping",
        python_callable=link_scrape
    )

    handle_rescheduling_op = PythonOperator(
        task_id="handle_rescheduling",
        python_callable=handle_rescheduling
    )

    empty_op = EmptyOperator(task_id="list_empty")


    def placeholder_before_stats():
        print("Stats calculation will begin shortly...")


    empty_op_2 = PythonOperator(
        task_id="placeholder_operator_before_stats",
        python_callable=placeholder_before_stats
    )

    branch_op = branch_func()

    # branch_op >> [empty_op, link_scraping_op, handle_rescheduling_op]
    branch_op >> [empty_op, link_scraping_op, empty_op_2]

    empty_op_2 >> decade_operators

    for index, decade in enumerate(decade_operators):
        decade >> decade_gender_operators[index]

    for decade_gender in decade_gender_operators:
        decade_gender >> handle_rescheduling_op
