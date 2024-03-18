from database import Database
from api import APIClient
import logging

logger = logging.getLogger('ETL Logger')
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


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
    api_key = 'your_api_key_here' # This is not needed as of now because of using publick API but is need in APIs that need authentication
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


if __name__ == "__main__":
    main()
