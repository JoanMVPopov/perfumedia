import ast
import os

from airflow.decorators import task
from airflow.models import DagModel
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta

from matplotlib.ticker import MaxNLocator

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
        max_active_tasks=3
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


    def get_category_avg_pie_chart(df, category='type', threshold=1):
        categories = df[category].apply(lambda x: ast.literal_eval(x))
        numbers = df[f'{category}_numbers'].apply(lambda x: ast.literal_eval(x))

        dictionary = dict()

        for i, category_list in enumerate(categories):
            for j, category_j in enumerate(category_list):
                # if falsy value (still not in dictionary)
                if not dictionary.get(category_j):
                    dictionary[category_j] = numbers.iloc[i][j]
                else:
                    dictionary[category_j] += numbers.iloc[i][j]


        # get the average per category
        avg_dict = {key: (value / len(categories)) for key, value in dictionary.items()}

        filtered_dict = {}
        small_value_sum = 0

        for key, value in avg_dict.items():
            if value < threshold:
                small_value_sum += value  # Add small values to 'Others'
            else:
                filtered_dict[key] = value

        if small_value_sum > 0:
            filtered_dict['Others'] = small_value_sum

        return filtered_dict


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

            if df.empty or df_filtered.empty:
                print("DataFrame is empty!")
                return

            df_filtered_rubrics_only = df_filtered[['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']]

            # Calculate statistics
            summary = df_filtered_rubrics_only.describe()
            median = df_filtered_rubrics_only.median()
            # if multiple modes, select first one
            mode = df_filtered_rubrics_only.mode().iloc[0]

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
            sns.boxplot(data=df_filtered_rubrics_only)
            plt.title("Box Plots of Ratings")

            file_name = f'{decade}_{gender}_box_plots.png'
            file_path_box_plots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_box_plots, bbox_inches='tight')

            # QQ Plots
            fig, axes = plt.subplots(len(df_filtered_rubrics_only.columns), 1, figsize=(6, 14))
            for i, col in enumerate(df_filtered_rubrics_only.columns):
                #print(df_filtered_rubrics_only[col])
                stats.probplot(df_filtered_rubrics_only[col], dist="norm", plot=axes[i])
                axes[i].set_title(f"QQ Plot for {col}")
                axes[i].set_xlabel("Ordered value quantiles")
                axes[i].set_xlabel("Normal quantiles")
            plt.tight_layout()

            file_name = f'{decade}_{gender}_qq_plots.png'
            file_path_qq_plots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_qq_plots, bbox_inches='tight')

            # Pairplot with histograms
            g = sns.pairplot(df_filtered_rubrics_only, corner=True, diag_kind=None)

            # Replace diagonal elements with custom histograms
            for i in range(len(df_filtered_rubrics_only.columns)):
                ax = g.axes[i, i]  # Access the diagonal subplot
                if ax is not None:  # Check if the axis exists
                    g.fig.delaxes(ax)  # Remove the existing axis
                    new_ax = g.fig.add_subplot(len(df_filtered_rubrics_only.columns), len(df_filtered_rubrics_only.columns),
                                               i * len(df_filtered_rubrics_only.columns) + i + 1)  # Recreate axis

                    ax = sns.histplot(df_filtered_rubrics_only.iloc[:, i], bins=15, kde=False, ax=new_ax,
                                      color="skyblue")  # Add histogram
                    ax.set_title(f"Histogram of {df_filtered_rubrics_only.columns[i]}", fontsize=10, fontweight='bold')  # Add title

            g.fig.subplots_adjust(hspace=0.5, wspace=0.5)

            file_name = f'{decade}_{gender}_pairplots.png'
            file_path_pairplots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_pairplots, bbox_inches='tight')

            # Violin Plot
            plt.figure(figsize=(8, 6))
            sns.violinplot(data=df_filtered_rubrics_only)
            plt.title("Violin Plots of Ratings")

            file_name = f'{decade}_{gender}_violin_plots.png'
            file_path_violin_plots = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_violin_plots, bbox_inches='tight')

            #############
            ## NOTES HISTOGRAM
            #############

            notes = df_filtered['notes'].apply(lambda x: ast.literal_eval(x))

            dictionary_notes = dict()

            for note_list in notes:
                for current_note in note_list:
                    if not dictionary_notes.get(current_note):
                        dictionary_notes[current_note] = 1
                    else:
                        dictionary_notes[current_note] += 1

            num_unique_notes = len(dictionary_notes)
            n = 25 if num_unique_notes > 25 else num_unique_notes

            # select top n most frequently used notes (since it would not look nice if we displayed all notes)
            top_notes = sorted(dictionary_notes.items(), key=lambda x: x[1], reverse=True)[:n]

            notes = [item[0] for item in top_notes]
            values = [item[1] for item in top_notes]

            plt.figure(figsize=(16, 8))
            plt.bar(notes, values, color="#C96868")
            plt.xlabel('Notes')
            plt.ylabel('Number of perfumes')
            plt.title(f'Top {n} most frequently used notes')

            # force y-axis to display only rounded numbers
            plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

            plt.tight_layout()

            plt.subplots_adjust(bottom=0.25)  # Increase the bottom margin

            # add text below the x-axis label
            plt.figtext(0.5, 0.05, f'Total number of unique notes in dataset: {num_unique_notes}', ha='center', fontsize=14)

            # rotate ticks to reduce text overlap
            plt.xticks(rotation=45, ha="right", fontsize=8)

            file_name = f'{decade}_{gender}_notes_histogram.png'
            file_path_notes_histogram = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_notes_histogram, bbox_inches='tight')

            #############
            ## PIE CHARTS
            #############

            categories = ['type', 'style', 'season', 'occasion']
            threshold = 1

            fig, axs = plt.subplots(4, 1, figsize=(12, 36))

            for i, category in enumerate(categories):
                dictionary = get_category_avg_pie_chart(df_filtered, category, threshold)

                # create a pie chart from the dictionary values
                labels = dictionary.keys()
                sizes = dictionary.values()

                axs[i].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
                axs[i].set_title(f'Pie Chart of average {category} values')

                if 'Others' in dictionary:
                    fig.text(0.5, 0.01, f'"Others" includes categories below the threshold of {threshold}% per pie',
                                ha='center', fontsize=10, color='gray')


            plt.tight_layout()
            file_name = f'{decade}_{gender}_avg_categories_piecharts.png'
            file_path_categories_piecharts = os.path.join(current_dir, folder_name, file_name)
            plt.savefig(file_path_categories_piecharts, bbox_inches='tight')

            ##############
            ## PROGRESSION
            ##############

            # only do it for all decades, per gender since info is not enough for further granularity
            if decade == 'All':
                # reset index otherwise rel_year becomes index
                # selects all 5 rubric columns + years and excludes everything else
                df_agg = df_filtered.groupby('rel_year')[['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']].agg(['mean', 'std']).reset_index()

                # if year has only 1 record, std will be NaN and the graph will look funny
                df_agg.fillna(0.1, inplace=True)

                fig, axs = plt.subplots(5, 1, figsize=(12, 30))

                # range 5 because of 5 rubrics
                for i in range(5):
                    axs[i].plot(df_agg.iloc[:, 0], df_agg.iloc[:, 2 * i + 1], label='Mean Value', color='#C96868',
                             linewidth=2, marker='o')

                    # adding the shaded region for std
                    axs[i].fill_between(df_agg.iloc[:, 0],
                                     df_agg.iloc[:, 2 * i + 1] - df_agg.iloc[:, 2 * i + 2],
                                     df_agg.iloc[:, 2 * i + 1] + df_agg.iloc[:, 2 * i + 2],
                                     color='#FFF4EA', alpha=1, label='±1 Std. Dev.')

                    axs[i].set_title(f'Yearly Averages with Standard Deviation for {df_agg.columns[2 * i + 1][0]}', fontsize=16)
                    axs[i].set_xlabel('Year', fontsize=12)
                    axs[i].set_ylabel('Average Value', fontsize=12)
                    plt.legend(fontsize=12)
                    plt.grid(alpha=0.3)

                plt.tight_layout()

                file_name = f'{decade}_{gender}_avg_rubric_progression.png'
                file_path_rubric_progression = os.path.join(current_dir, folder_name, file_name)
                plt.savefig(file_path_rubric_progression, bbox_inches='tight')

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
