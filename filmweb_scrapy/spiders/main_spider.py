import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'

    def parse(self, response, **kwargs):
        ...