#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import json
import shutil
import time
import datetime

from country import Country
from city import City
from sender import Sender
from card import Card

CONFIG_DB_FILENAME = 'db.filename'

RAW_COUNTRIES = 'countries'
RAW_CITIES = 'cities'
RAW_SENDERS = 'senders'
RAW_CARDS = 'cards'

COUNTRY_ENAME = 'ename'
COUNTRY_NAME = 'name'
CITY_ENAME = 'ename'
CITY_NAME = 'name'
CITY_COUNTRY = 'country'
SENDER_NAME = 'name'
CARD_SENDERS = 'senders'
CARD_CITY = 'city'
CARD_DATES = 'dates'
CARD_POSITION = 'position'

DB_READ_ERROR = 'DBRead'

class DB:
    def __init__(self, config_file_name='db.cfg'):
        self.config = json.load(open(config_file_name))

        self.countries = list()
        self.cities = list()
        self.senders = list()
        self.cards = list()

        raw_db = json.load(open(self.config[CONFIG_DB_FILENAME]))

        if RAW_COUNTRIES in raw_db:
            for x in raw_db[RAW_COUNTRIES]:
                if not self.find_country(x[COUNTRY_ENAME]):
                    self.add_country(x[COUNTRY_ENAME], x[COUNTRY_NAME])
                else:
                    print(DB_READ_ERROR, 'DoubleCountry', x)
        if RAW_CITIES in raw_db:
            for x in raw_db[RAW_CITIES]:
                country = self.find_country(x[CITY_COUNTRY])
                if country:
                    if not self.find_city(x[CITY_ENAME]):
                        self.add_city(x[COUNTRY_ENAME], x[COUNTRY_NAME], country)
                    else:
                        print(DB_READ_ERROR, 'DoubleCity', x)
                else:
                    print(DB_READ_ERROR, 'NoCountry', x)
        if RAW_SENDERS in raw_db:
            for x in raw_db[RAW_SENDERS]:
                sender = self.find_sender(x[SENDER_NAME])
                if sender:
                    print('DBRead', 'DoubleSender', x)
                else:
                    self.add_sender(x[SENDER_NAME])
        if RAW_CARDS in raw_db:
            for x in raw_db[RAW_CARDS]:
                city = self.find_city(x[CARD_CITY])
                if not city:
                    print(DB_READ_ERROR, 'NoCity')
                    continue
                senders = list()
                for sender in x[CARD_SENDERS]:
                    sender = self.find_sender(sender)
                    if sender:
                        senders.append(sender)
                    else:
                        print(DB_READ_ERROR, 'NoSender', x)
                        senders.clear()
                        break
                self.add_card(city, senders,
                              datetime.date(**x[CARD_DATES][0]),
                              datetime.date(**x[CARD_DATES][1]),
                              x[CARD_POSITION])

        self.changes = False

    def __del__(self):
        if self.changes:
            shutil.copy(self.config[CONFIG_DB_FILENAME],
                        "OLD/" + self.config[CONFIG_DB_FILENAME] + "." + str(int(time.time())))

        result = {RAW_COUNTRIES: [self.to_json_country(x) for x in self.countries],
                  RAW_CITIES: [self.to_json_city(x) for x in self.cities],
                  RAW_SENDERS: [self.to_json_sender(x) for x in self.senders],
                  RAW_CARDS: [self.to_json_card(x) for x in self.cards]}
        json.dump(result, open(self.config[CONFIG_DB_FILENAME], "wt"), sort_keys=True, indent=1, ensure_ascii=False)

    def __exit__(self, exp_type, exp_value, traceback):
        pass

    def __enter__(self):
        return self

    def find_country_by_name(self, name):
        result = [x for x in self.countries if x.name == name]
        if len(result) == 1:
            return result[0]
        return None

    def find_country(self, ename):
        result = [x for x in self.countries if x.ename == ename]
        if len(result) == 1:
            return result[0]
        return None

    def find_city_by_name(self, name):
        result = [x for x in self.cities if x.name == name]
        if len(result) > 0:
            return result
        return None

    def find_city(self, ename):
        result = [x for x in self.cities if x.ename == ename]
        if len(result) == 1:
            return result[0]
        return None

    def add_country(self, ename, name):
        self.changes = True
        self.countries.append(Country(ename, name))
        return self.countries[-1]

    def add_city(self, ename, name, country):
        self.changes = True
        city = City(ename, name, country)
        country.add_city(city)
        self.cities.append(city)
        return self.cities[-1]

    def find_sender(self, name):
        result = [x for x in self.senders if x.name == name]
        if len(result) == 1:
            return result[0]
        return None

    def add_sender(self, name):
        self.changes = True
        self.senders.append(Sender(name))
        return self.senders[-1]

    def add_card(self, city, senders, sent, received, geo):
        self.changes = True
        card = Card(city, senders, sent, received, geo)
        self.cards.append(card)
        city.add_card(city)
        for sender in senders:
            sender.add_card(card)
        return card

    @staticmethod
    def to_json_country(country):
        assert isinstance(country, Country)
        return {COUNTRY_ENAME: country.ename, COUNTRY_NAME: country.name}

    @staticmethod
    def to_json_city(city):
        assert isinstance(city, City)
        return {CITY_ENAME: city.ename, CITY_NAME: city.name, CITY_COUNTRY: city.country.ename}

    @staticmethod
    def to_json_sender(sender):
        assert isinstance(sender, Sender)
        return {SENDER_NAME: sender.name}

    @staticmethod
    def to_json_card(card):
        assert isinstance(card, Card)
        return {CARD_CITY: card.city.ename,
                CARD_DATES: [{'year': x.year, 'month': x.month, 'day': x.day} for x in (card.start, card.finish)],
                CARD_POSITION: card.position,
                CARD_SENDERS: [x.name for x in card.senders]}
