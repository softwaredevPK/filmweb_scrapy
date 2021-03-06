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


def movie_length_vs_rating_with_stats(min_len=5):

    def get_random_color():
        return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    query = db_manager.session.query(Movie)
    df = pd.read_sql(query.statement, query.session.bind) # todo dlaczego pusty df
    if df.empty:
        return
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
    fig, ax = plt.subplots()
    for i, genre in enumerate(df.genre.unique()):
        sub_df = df[df['genre'] == genre]
        sub_df_len = len(sub_df)
        if sub_df_len > min_len:
            plt.scatter(sub_df['length'].to_numpy(),  sub_df['rating'].to_numpy(),
                        color=colors[i] if i < len(colors) - 1 else get_random_color(),
                        label=f'{genre}: {sub_df_len}')
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', borderaxespad=0.)
    ax.grid(True)
    ax.set_title("Movie lenght vs rating ")
    ax.set_xlabel("Length")
    ax.set_ylabel("Rating")
    plt.tight_layout()


def actor_rating_vs_movie_rating():
    final_actor_ratings = np.array([])
    final_movie_ratings = np.array([])
    query = db_manager.session.query(Actor)
    df_actors = pd.read_sql(query.statement, query.session.bind)
    query = db_manager.session.query(Movie)
    df_movies = pd.read_sql(query.statement, query.session.bind)
    for _, movie in df_movies.iterrows():
        movie_actors_df = df_actors[df_actors['movies'].str.contains(movie.title)]
        ratings = movie_actors_df['rating']
        final_actor_ratings = np.append(final_actor_ratings, ratings)
        final_movie_ratings = np.append(final_movie_ratings, [movie.rating for i in range(len(movie_actors_df))])
    fig, ax = plt.subplots()
    plt.scatter(final_actor_ratings, final_movie_ratings)
    ax.grid(True)
    ax.set_title("Actor rating vs Movie rating")
    ax.set_xlabel("Actor Rating")
    ax.set_ylabel("Movie Rating")
    plt.tight_layout()


most_movies_by_director()
most_movies_by_director(10)
movie_length_vs_rating_with_stats()
actor_rating_vs_movie_rating()

