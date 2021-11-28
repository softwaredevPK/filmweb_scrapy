from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import column_property, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text, )
from scrapy.utils.project import get_project_settings
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
        dal.conn_string = r"sqlite:///filmweb.db"
        dal.echo = True
        dal.connect()
        self.session = dal.session_maker()


association_table = Table('association', Base.metadata,
    Column('actors_id', ForeignKey('actors.id')),
    Column('movies_id', ForeignKey('movies.id'))
)


class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    height = Column(Integer)
    rating = Column(Float(decimal_return_scale=1))
    # movie = relationship("Movie", backref="director")


class Actor(Director):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    height = Column(Integer)
    rating = Column(Float(decimal_return_scale=1))


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    rating = Column(Float(decimal_return_scale=1))
    genre = Column(String)
    director_id = Column(ForeignKey('directors.id'))
    publish_year = Column(Integer)
    length = Column(DateTime)
    critics_rating = Column(Float(decimal_return_scale=1))
    actors = relationship('Actor', secondary=association_table, backref='movies')


db_manager = DBManager()
