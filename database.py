from sqlalchemy import create_engine, Column, Integer, String, Boolean, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('ETL Logger')

metadata = MetaData()

search_terms_table = Table(
    'search_terms', metadata,
    Column('id', Integer, primary_key=True),
    Column('term', String),
    Column('value', String)
)

news_data_table = Table(
    'news_data', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('url', String),
    Column('image_url', String),
    Column('summary', String),
    Column('published_at', String),
    Column('updated_at', String),
    Column('featured', Boolean),
    Column('news_site', String)
)


class Database:
    def __init__(self, db_name='news_data.sqlite'):
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def create_tables(self):
        metadata.create_all(self.engine)

    def insert_search_term(self, term, value):
        # Check if the value already exists
        existing_term = self.session.query(search_terms_table).filter_by(value=value).first()
        if existing_term:
            logger.info(f"Term with value '{value}' already exists.")
            return  # Skip insertion

        # Insert the new term
        new_term = search_terms_table.insert().values(term=term, value=value)
        try:
            self.session.execute(new_term)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            logger.error("Failed to insert term due to integrity error.")

    def get_search_terms(self):
        return self.session.query(search_terms_table).all()

    def insert_api_data(self, data_list):
        try:
            news_data = []
            for data in data_list:
                news_data.append({
                    'title': data['title'],
                    'url': data['url'],
                    'image_url': data['image_url'],
                    'summary': data['summary'],
                    'published_at': data['published_at'],
                    'updated_at': data['updated_at'],
                    'featured': data['featured'],
                    'news_site': data['news_site']
                })
            self.session.execute(news_data_table.insert(), news_data)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to insert data: {str(e)}")

    @classmethod
    def get_engine(cls):
        return create_engine('sqlite:///news_data.sqlite')
