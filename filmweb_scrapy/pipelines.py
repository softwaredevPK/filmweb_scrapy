from .items import ActorItem, DirectorItem, MovieItem
from .models import Actor, Director, Movie, db_manager


class FilmwebScrapyPipeline:
    def process_item(self, item, spider):
        if type(item) is DirectorItem:
            self.process_director_item(item, spider)
        elif type(item) is MovieItem:
            self.process_movie_item(item, spider)
        elif type(item) is ActorItem:
            self.process_actor_item(item, spider)
        return item

    def process_director_item(self, item, spider):
        fullname = item.get("fullname")
        director = self.get_director(fullname)
        if not director:
            director = Director()
            director.fullname = fullname
            director.birth_date = item.get("birth_date")
            director.birth_place = item.get("birth_place")
            director.birth_country = item.get("birth_country")
            director.height = item.get("height")
            director.rating = item.get("rating")
            director.movies = item.get("movie") if item.get("movie") else ""
            db_manager.session.add(director)
        elif director and item.get("movie"):
            director.movies = director.movies + "|" + item.get("movie")
        db_manager.session.commit()

    def process_actor_item(self, item, spider):
        fullname = item.get("fullname")
        actor = self.get_actor(fullname)
        if not actor:
            actor = Actor()
            actor.fullname = item.get("fullname")
            actor.birth_date = item.get("birth_date")
            actor.birth_place = item.get("birth_place")
            actor.birth_country = item.get("birth_country")
            actor.height = item.get("height")
            actor.rating = item.get("rating")
            actor.movies = item.get("movie") if item.get("movie") else ""
            db_manager.session.add(actor)
        elif actor and item.get("movie"):
            actor.movies = actor.movies + "|" + item.get("movie")
        db_manager.session.commit()

    def process_movie_item(self, item, spider):
        title = item["title"]
        movie = self.get_movie(title)
        if not movie:
            movie = Movie()
            movie.title = item["title"]
            movie.rating = item["rating"]
            movie.genre = item["genre"]
            movie.publish_year = item["publish_year"]
            movie.length = item["length"]
            movie.critics_rating = item["critics_rating"]
            db_manager.session.add(movie)
            db_manager.session.commit()

    @staticmethod
    def get_director(fullname):
        return db_manager.session.query(Director).filter(Director.fullname == fullname).one_or_none()

    @staticmethod
    def get_actor(fullname):
        return db_manager.session.query(Actor).filter(Actor.fullname == fullname).one_or_none()

    @staticmethod
    def get_movie(title):
        return db_manager.session.query(Movie).filter(Movie.title == title).one_or_none()
