import ast
import os
from datetime import datetime, timedelta

import pandas as pd
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.models.variable import Variable
from airflow.models.dag import DAG
from airflow.models import DagModel
from airflow.providers.postgres.hooks.postgres import PostgresHook
from utilities.ETLScraper import extract
from airflow.utils.dates import days_ago

from utilities.basic_analysis import calculate_basic_stats_and_diagrams
from utilities.brands_basic_rubrics_stats import calculate_basic_brand_rubric_stats_table
from utilities.categories_avg_piecharts import get_avg_categories_piecharts
from utilities.correlation import calculate_correlation_and_graphs
from utilities.dimens_reduc_and_clustering import reduce_and_cluster
from utilities.notes_histograms import get_histograms_for_notes
from utilities.rubric_progression_plots import calculate_rubric_progression_throughout_decades

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'email': ['mamaegalabar4@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(0)
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline using Selenium and Airflow with CeleryExecutor',
    # IMPORTANT
    schedule_interval='*/10 * * * *',  # every 10 minutes
    catchup=False,
    max_active_runs=1,
    max_active_tasks=3,
    is_paused_upon_creation=True
) as etl_dag:

    @task.branch(task_id='etl_branch')
    def etl_branch_func():
        pg_hook = PostgresHook(postgres_conn_id='dag_connection')
        connection = pg_hook.get_conn()
        cursor = connection.cursor()

        get_query = """
                    SELECT COUNT(*) from etl_backlog
                    """
        cursor.execute(get_query)
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if count == 0:
            #return "pause_etl_execution"
            return "placeholder_operator_before_stats"
        else:
            return "extract_data"

    def pause_execution():
        dag: DagModel = DagModel.get_dagmodel('etl_pipeline')
        dag.set_is_paused(True)

        # Save time at which we have finished processing the Backlog
        current_time = datetime.now()
        datetime_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
        Variable.set("time_etl_completion", datetime_string)
        return


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

        # if the style leans toward selected gender, return the row
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

            df_filtered = df_filtered.reset_index(drop=True)

            # Get basic stats (mean, median, mode, etc.) in a table format
            # Also create Boxplots, QQ plots, Violin plots, Pairplot
            calculate_basic_stats_and_diagrams(decade, gender, df_filtered,
                                               current_dir, folder_name)

            # Notes histograms
            get_histograms_for_notes(decade, gender, df_filtered, 25,
                                     current_dir, folder_name)

            categories = ['type', 'style', 'season', 'occasion']

            # Pie charts
            get_avg_categories_piecharts(decade, gender, df_filtered, 1,
                                         categories, current_dir, folder_name)

            # Correlation tables
            calculate_correlation_and_graphs(decade, gender, df_filtered, 50,
                                             categories, current_dir, folder_name)

            # Brands table
            calculate_basic_brand_rubric_stats_table(decade, gender, df_filtered, 10,
                                                     current_dir, folder_name)

            # Rubrics progression
            # only do it for all decades, per gender, since info is not enough for further granularity
            if decade == 'All':
                calculate_rubric_progression_throughout_decades(decade, gender, df_filtered,
                                                                current_dir, folder_name)

                # DIMENSIONALITY REDUCTION & CLUSTERING

                rating_names = ['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']

                reduce_and_cluster(df_filtered, categories, rating_names,
                                   decade, gender, current_dir, folder_name)

        except Exception as e:
            print(e)
        finally:
            return


    from airflow.providers.postgres.hooks.postgres import PostgresHook


    def placeholder_before_stats():
        print("Stats calculation will begin shortly...")
        print("Wiping cluster information...")

        connection = None
        cursor = None

        try:
            pg_hook = PostgresHook(postgres_conn_id='dag_connection')
            connection = pg_hook.get_conn()
            cursor = connection.cursor()

            cursor.execute("TRUNCATE TABLE etl_clusters")

            connection.commit()

            # verify it's empty
            cursor.execute("SELECT COUNT(*) FROM etl_clusters")
            count = cursor.fetchone()[0]

            assert count == 0, "Cluster info was not wiped correctly"

            print("Wiping completed. Analysis will begin soon...")
        except Exception as e:
            print("Error during stats prep:", e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract,
    )

    pause_task = PythonOperator(
        task_id='pause_etl_execution',
        python_callable=pause_execution,
    )

    empty_op_2 = PythonOperator(
        task_id="placeholder_operator_before_stats",
        python_callable=placeholder_before_stats
    )

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

    branch_op = etl_branch_func()

    # branch_op >> [pause_task, extract_task]
    branch_op >> [empty_op_2, extract_task]

    empty_op_2 >> decade_operators

    for index, decade in enumerate(decade_operators):
        decade >> decade_gender_operators[index]

    for decade_gender in decade_gender_operators:
        decade_gender >> pause_task

    # All masculine before All feminine and All All
    decade_gender_operators[4][0] >> [decade_gender_operators[4][1], decade_gender_operators[4][2]]
    # All feminine before All All
    decade_gender_operators[4][1] >> decade_gender_operators[4][2]
