import datetime
import re

import scrapy
from itemloaders.processors import MapCompose


def to_datetime(value):
    if re.match(r"^\d{4}$", value):
        return datetime.datetime.strptime(value, "%Y")
    elif re.match(r"^\d{4}-\d{2}$", value):
        return datetime.datetime.strptime(value, "%Y-%m")
    elif re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return datetime.datetime.strptime(value, "%Y-%m-%d")
    else:
        return None


def space_split_first_value(value):
    try:
        return value.split(" ")[0]
    except IndexError:
        return ""


def coma_split_first_value(value):
    try:
        return value.split(",")[0]
    except IndexError:
        return ""


def coma_split_last_value(value):
    try:
        return value.split(",")[-1]
    except IndexError:
        return ""


def comma_to_dot(value):
    return value.replace(",", ".")


class PersonItem(scrapy.Item):
    """Abstract Item"""

    birth_date = scrapy.Field(input_processor=MapCompose(to_datetime))
    birth_place = scrapy.Field(input_processor=MapCompose(coma_split_first_value, str.strip))
    birth_country = scrapy.Field(input_processor=MapCompose(str.strip, coma_split_last_value, str.strip))
    height = scrapy.Field(input_processor=MapCompose(space_split_first_value, int))
    rating = scrapy.Field(input_processor=MapCompose(comma_to_dot, float))
    movie = scrapy.Field()
    fullname = scrapy.Field(input_processor=MapCompose(str.strip))


class DirectorItem(PersonItem):
    pass


class ActorItem(PersonItem):
    pass


class MovieItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(str.strip))
    rating = scrapy.Field(input_processor=MapCompose(comma_to_dot, float))
    genre = scrapy.Field(input_processor=MapCompose(str.strip))
    publish_year = scrapy.Field(input_processor=MapCompose(str.strip, int))
    length = scrapy.Field(input_processor=MapCompose(str.strip, int))
    critics_rating = scrapy.Field(input_processor=MapCompose(comma_to_dot, float))
    director_name = scrapy.Field(input_processor=MapCompose(str.strip))
    director_surname = scrapy.Field(input_processor=MapCompose(str.strip))
