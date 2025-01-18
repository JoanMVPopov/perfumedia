import ast
import os

from airflow.decorators import task
from airflow.models import DagModel
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
from utilities.ListLinkScraper import link_scrape
from airflow.utils.dates import days_ago
from airflow.models.variable import Variable
from utilities.ssh_tunnel import transmit_data_through_ssh_tunnel


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
            # etl running, so do not scrape more links
            return 'list_empty'

        # 3 for the 3 days of scraping in total
        # if times_ran < 3:
        if times_ran < 1:
            return 'link_scraping'
        # if we have scraped all the links from all 3 days
        else:
            return 'handle_rescheduling'
            # return 'placeholder_operator_before_stats'


    def handle_rescheduling():
        # TODO: Need to figure out a default return value
        time_etl_completion = datetime.strptime(Variable.get("time_etl_completion"), "%Y-%m-%d %H:%M:%S")
        # delta = timedelta(days=5) or (days=7)
        delta = timedelta(minutes=30)

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


    branch_op = branch_func()

    branch_op >> [empty_op, link_scraping_op, handle_rescheduling_op]
    # branch_op >> [empty_op, link_scraping_op, empty_op_2]


