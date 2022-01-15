from sqlalchemy import (Column, Date, Float, Integer, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import func

from .utils import SingleInstanceClass

Base = declarative_base()


class DataAccessLayer(SingleInstanceClass):
    """Class to manage access to DB"""

    def __init__(self):
        self.conn_string = None
        self.echo = None
        self.engine = None
        self.session_maker = None
        self.session = None

    def connect(self):
        self.engine = create_engine(self.conn_string, echo=self.echo)
        Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(bind=self.engine)


class DBManager:
    def __init__(self):
        dal = DataAccessLayer()
        dal.conn_string = r"sqlite:///filmweb1.db"
        dal.echo = False
        dal.connect()
        self.session = dal.session_maker()

    def get_director_movies(self, name: str):
        try:
            director = self.session.query(Director).filter(func.lower(Director.fullname).contains(name.lower())).one()
        except MultipleResultsFound:
            raise ValueError("Multiple Directors found for given name")
        movies = [movie.strip().lower() for movie in director.movies.split('|')]
        return self.session.query(Movie).filter(func.lower(Movie.title).in_(movies)).all()

    def get_actor_movies(self, name: str):
        try:
            actor = self.session.query(Actor).filter(func.lower(Actor.fullname).contains(name.lower())).one()
        except MultipleResultsFound:
            raise ValueError("Multiple Directors found for given name")
        movies = [movie.strip().lower() for movie in actor.movies.split('|')]
        return self.session.query(Movie).filter(func.lower(Movie.title).in_(movies)).all()

    def get_most_popular_movies(self, limit=10):
        return self.session.query(Movie).order_by(Movie.rating.desc()).limit(limit).all()


class Director(Base):
    __tablename__ = "directors"

    fullname = Column(String, primary_key=True)
    birth_date = Column(Date)
    birth_place = Column(String)
    birth_country = Column(String)
    height = Column(Integer)
    rating = Column(Float(decimal_return_scale=1))
    movies = Column(String)  # title of movies that it's related to, separated by |


class Actor(Base):
    __tablename__ = "actors"

    fullname = Column(String, primary_key=True)
    birth_date = Column(Date)
    birth_place = Column(String)
    birth_country = Column(String)
    height = Column(Integer)
    rating = Column(Float(decimal_return_scale=1))
    movies = Column(String)  # title of movies that it's related to, separated by |


class Movie(Base):
    __tablename__ = "movies"

    title = Column(String, primary_key=True)
    rating = Column(Float(decimal_return_scale=1))
    genre = Column(String)
    publish_year = Column(Integer)
    length = Column(Integer)
    critics_rating = Column(Float(decimal_return_scale=1))


db_manager = DBManager()
