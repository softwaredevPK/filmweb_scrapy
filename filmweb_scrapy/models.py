from sqlalchemy import (Column, Date, Float, Integer, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
