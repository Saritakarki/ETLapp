from api import APIClient
import requests
from database import Database, news_data_table


api_client = APIClient()
db = Database(db_name='news_data.sqlite')


def test_api():
    api_url = api_client.url
    response = requests.get(api_url)
    assert response.status_code == 200
    assert response.json() is not None


def test_integration_fetch_insert_api_data():
    data = api_client.fetch_api_data(search_term={'news_site': 'NASA'})
    assert data is not None
    assert 'results' in data

    engine = Database.get_engine()
    Database.create_tables(engine)
    db.insert_api_data(data['results'])
    data_count = db.session.query(news_data_table).count()
    assert data_count > 0

