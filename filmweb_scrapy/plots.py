import numpy as np
import matplotlib.pyplot as plt
from .models import db_manager, Director, Movie, Actor


def most_movies_by_director(limit=None):
    """limit: int Limit number of movies on"""
    # plt settings
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots()

    query = db_manager.session.query(Director)
    if limit:
        query = query.limit(limit)
    director_movies = {director.fullname: len(director.movies.split('|')) for director in query.all()}
    director_data = list(director_movies.values())
    director_names = list(director_movies.keys())
    ax.barh(director_names, director_data)
    ax.set(xlim=[0, max(director_data)], xlabel='Total number of movies', ylabel='Director',
           title='Number of created movies')

    print(f"Mean number of movies made by directors: {np.mean(director_data)}")
    fig.show()
