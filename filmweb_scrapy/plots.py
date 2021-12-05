import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from filmweb_scrapy.models import db_manager, Director, Movie, Actor
import pandas as pd
import random


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


def movie_length_vs_rating(min_len=5):

    def get_random_color():
        return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    query = db_manager.session.query(Movie)
    df = pd.read_sql(query.statement, query.session.bind)
    movies_by_genre = df.groupby(by='genre').describe().rating
    print(movies_by_genre)

    colors = ['#1f77b4',
              '#ff7f0e',
              '#2ca02c',
              '#d62728',
              '#9467bd',
              '#8c564b',
              '#e377c2',
              '#7f7f7f',
              '#bcbd22',
              '#17becf',
              '#ffd700',
              '#c0c0c0',
              "#990000",
              "#ff0000",
              ]
    for i, genre in enumerate(df.genre.unique()):
        sub_df = df[df['genre'] == genre]
        sub_df_len = len(sub_df)
        if sub_df_len > min_len:
            plt.scatter(sub_df['length'].to_numpy(),  sub_df['rating'].to_numpy(),
                        color=colors[i] if i < len(colors) - 1 else get_random_color(),
                        label=f'{genre}: {sub_df_len}')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', borderaxespad=0.)
    plt.grid(True)
    plt.title("Movie lenght vs rating ")
    plt.xlabel("Length")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.show()