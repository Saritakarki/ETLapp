from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('ETL Logger')

Base = declarative_base()


class SearchTerm(Base):
    __tablename__ = 'search_terms'

    id = Column(Integer, primary_key=True)
    term = Column(String)
    value = Column(String)


class NewsData(Base):
    __tablename__ = 'news_data'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    image_url = Column(String)
    summary = Column(String)
    published_at = Column(String)
    updated_at = Column(String)
    featured = Column(Boolean)
    news_site = Column(String)


class Database:
    def __init__(self, db_name='news_data.sqlite'):
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def insert_search_term(self, term, value):
        # Check if the value already exists
        existing_term = self.session.query(SearchTerm).filter_by(value=value).first()
        if existing_term:
            logger.info(f"Term with value '{value}' already exists.")
            return  # Skip insertion

        # Insert the new term
        new_term = SearchTerm(term=term, value=value)
        self.session.add(new_term)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            logger.error("Failed to insert term due to integrity error.")

    def get_search_terms(self):
        return self.session.query(SearchTerm).all()

    def insert_api_data(self, data_list):
        try:
            news_data = []
            for data in data_list:
                news_data.append(NewsData(
                    title=data['title'],
                    url=data['url'],
                    image_url=data['image_url'],
                    summary=data['summary'],
                    published_at=data['published_at'],
                    updated_at=data['updated_at'],
                    featured=data['featured'],
                    news_site=data['news_site']
                ))
            self.session.bulk_save_objects(news_data)

            # Commit the transaction
            self.session.commit()
        except Exception as e:
            # Rollback the transaction if an error occurs
            self.session.rollback()
            logger.error(f"Failed to insert data: {str(e)}")

    @classmethod
    def get_engine(cls):
        return create_engine('sqlite:///news_data.sqlite')
