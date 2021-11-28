import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from ..items import ActorItem, DirectorItem, MovieItem


class FilmwebSpider(scrapy.Spider):
    """
    Please run with below command to limit scrapped movie pages:
    scrapy crawl filmweb -a max_movies=int
    """

    name = "filmweb"

    start_urls = ["https://www.filmweb.pl/films/search/"]

    def __init__(self, max_movies=1, **kwargs):
        self.max_movies = int(max_movies)
        self.i = 0
        super().__init__(**kwargs)

    def parse(self, response, **kwargs):
        movies = response.css(".resultsList > li")
        for movie in movies:
            if self.i == self.max_movies:
                return
            movie_details_url = movie.css("a.filmPreview__link::attr(href)").get()
            yield scrapy.Request(response.urljoin(movie_details_url), self.parse_movie)
            self.i += 1
        next_page = response.css("li.pagination__item--next > a.pagination__link::attr(href)").get()
        yield scrapy.Request(response.urljoin(next_page), self.parse)

    def parse_movie(self, response, **kwargs):
        loader = ItemLoader(item=MovieItem(), selector=response)
        loader.default_output_processor = TakeFirst()
        title = response.css("h1.filmCoverSection__title span::text").get()
        loader.add_value("title", title)
        loader.add_css("publish_year", "span.filmCoverSection__year::text")
        loader.add_css("rating", "div.filmRating__rate span.filmRating__rateValue::text")
        loader.add_css("critics_rating", "div.filmRating--filmCritic > div > span.filmRating__rateValue::text")
        loader.add_css("genre", "div.filmInfo__info > span > a::text")
        loader.add_css("length", "span.filmCoverSection__filmTime::attr(data-duration)")

        meta = {"movie": title}

        director_url = response.css("div.filmInfo__info > a::attr(href)").get()
        yield scrapy.Request(response.urljoin(director_url), callback=self.parse_director, meta=meta, dont_filter=True)

        cast_url = response.css("section.FilmCastSection div.page__top a::attr(href)").get()
        yield scrapy.Request(response.urljoin(cast_url), callback=self.parse_cast, meta=meta, dont_filter=True)

        yield loader.load_item()

    def _parse_person(self, response, loader):
        """Parse data from /person url"""
        loader.add_css("birth_date", 'div.personPosterSection__infoData h3 span[itemprop="birthDate"]::attr(content)')
        loader.add_css("birth_place", 'div.personPosterSection__infoData h3 span[itemprop="birthPlace"]::text')
        loader.add_css("birth_country", 'div.personPosterSection__infoData h3 span[itemprop="birthPlace"]::text')
        loader.add_css("fullname", "h1.personCoverSection__title > a::attr(title)")

        loader.add_css("height", 'div.personPosterSection__infoData h3 span[itemprop="height"]::text')
        loader.add_css("rating", "span.personRating__rate::text")

    def parse_director(self, response, **kwargs):
        loader = ItemLoader(item=DirectorItem(), selector=response)
        loader.default_output_processor = TakeFirst()
        self._parse_person(response, loader)
        loader.add_value("movie", response.meta["movie"])
        yield loader.load_item()

    def parse_actor(self, response, **kwargs):
        loader = ItemLoader(item=ActorItem(), selector=response)
        loader.default_output_processor = TakeFirst()
        self._parse_person(response, loader)
        loader.add_value("movie", response.meta["movie"])
        yield loader.load_item()

    def parse_cast(self, response, **kwargs):
        actor_urls = response.css(
            "div.filmFullCastSection__list > div > div.castRoleListElement__info > a::attr(href)"
        ).getall()
        meta = response.meta
        for actor_url in actor_urls:
            yield scrapy.Request(response.urljoin(actor_url), callback=self.parse_actor, meta=meta)
