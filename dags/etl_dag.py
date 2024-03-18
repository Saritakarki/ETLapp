from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from app.database import Database
from app.api import APIClient
import logging

logger = logging.getLogger('ETL Logger')
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_workflow',
    default_args=default_args,
    description='A DAG to perform ETL tasks',
    schedule_interval=timedelta(days=1),  # Runs the task daily
)


def create_tables():
    # Create tables if they don't exist
    engine = Database.get_engine()
    Database.create_tables(engine)


def insert_search_terms():
    # Insert search terms into the database
    with Database() as db:
        db.insert_search_term('news_site', 'NASA')
        db.insert_search_term('featured', 'False')


def main():
    logger.info('Creating Tables if they don\'t exist.')
    create_tables()

    logger.info('Inserting search terms..')
    insert_search_terms()

    # Call API
    api_key = 'your_api_key_here' # This is not needed as of now because of using public API but is needed in APIs that need authentication
    client = APIClient(api_key)

    # Fetch search terms from database and call API for each term
    logger.info('Fetching Data From API..')
    with Database() as db:
        search_terms = db.get_search_terms()
        for term in search_terms:
            data = client.fetch_api_data({term.term: term.value})
            logger.info('Successfully Fetched Data From API!')
            if data:
                logger.info('Inserting Data into Database..')
                db.insert_api_data(data['results'])
        logger.info('Successfully Inserted Data!!')


run_etl = PythonOperator(
    task_id='run_etl',
    python_callable=main,
    dag=dag,
)


run_etl
