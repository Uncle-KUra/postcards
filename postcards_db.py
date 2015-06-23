#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import json
import shutil
import time

from country import Country
from city import City
from sender import Sender

CONFIG_DB_FILENAME = 'db.filename'

RAW_COUNTRIES = 'countries'
RAW_CITIES = 'cities'
RAW_SENDERS = 'senders'

COUNTRY_ENAME = 'ename'
COUNTRY_NAME = 'name'
CITY_ENAME = 'ename'
CITY_NAME = 'name'
CITY_COUNTRY = 'country'
SENDER_NAME = 'name'


class DB:
    def __init__(self, config_file_name='db.cfg'):
        self.config = json.load(open(config_file_name))

        self.countries = list()
        self.cities = list()
        self.senders = list()

        raw_db = json.load(open(self.config[CONFIG_DB_FILENAME]))

        if RAW_COUNTRIES in raw_db:
            for x in raw_db[RAW_COUNTRIES]:
                if not self.find_country(x[COUNTRY_ENAME]):
                    self.add_country(x[COUNTRY_ENAME], x[COUNTRY_NAME])
                else:
                    print('DBRead', 'DoubleCountry', x)
        if RAW_CITIES in raw_db:
            for x in raw_db[RAW_CITIES]:
                country = self.find_country(x[CITY_COUNTRY])
                if country:
                    if not self.find_city(x[CITY_ENAME]):
                        self.add_city(x[COUNTRY_ENAME], x[COUNTRY_NAME], country)
                    else:
                        print('DBRead', 'DoubleCity', x)
                else:
                    print('DBRead', 'NoCountry', x)
        if RAW_SENDERS in raw_db:
            for x in raw_db[RAW_SENDERS]:
                sender = self.find_sender(x[SENDER_NAME])
                if sender:
                    print('DBRead', 'DoubleSender', x)
                else:
                    self.add_sender(x[SENDER_NAME])

        self.changes = False

    def __del__(self):
        if self.changes:
            shutil.copy(self.config[CONFIG_DB_FILENAME],
                        "OLD/" + self.config[CONFIG_DB_FILENAME] + "." + str(int(time.time())))

        result = {RAW_COUNTRIES: [self.to_json_country(x) for x in self.countries],
                  RAW_CITIES: [self.to_json_city(x) for x in self.cities],
                  RAW_SENDERS: [self.to_json_sender(x) for x in self.senders]}
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
