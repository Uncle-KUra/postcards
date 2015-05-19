#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import json
import shutil
import time

from country import Country

CONFIG_DB_FILENAME = 'db.filename'

RAW_COUNTRIES = 'countries'

COUNTRY_ENAME = 'ename'
COUNTRY_NAME = 'name'


class DB:
    def __init__(self, config_file_name='db.cfg'):
        self.config = json.load(open(config_file_name))

        self.countries = list()

        raw_db = json.load(open(self.config[CONFIG_DB_FILENAME]))

        list(map(lambda x: self.add_country(x[COUNTRY_ENAME], x[COUNTRY_NAME]),
                 [x for x in raw_db[RAW_COUNTRIES] if self.find_country(x[COUNTRY_ENAME]) is None]))

        self.changes = False

    def __del__(self):
        if self.changes:
            shutil.copy(self.config[CONFIG_DB_FILENAME],
                        "OLD/" + self.config[CONFIG_DB_FILENAME] + "." + str(int(time.time())))

        result = {RAW_COUNTRIES: [self.to_json_country(x) for x in self.countries]}
        json.dump(result, open(self.config[CONFIG_DB_FILENAME], "wt"), sort_keys=True, indent=1, ensure_ascii=False)

    def __exit__(self, exp_type, exp_value, traceback):
        pass

    def __enter__(self):
        return self

    def find_country(self, name):
        result = [x for x in self.countries if x.name == name]
        if len(result) == 1:
            return result[0]
        return None

    def add_country(self, ename, name):
        self.changes = True
        self.countries.append(Country(ename, name))
        return self.countries[-1]

    @staticmethod
    def to_json_country(country):
        assert isinstance(country, Country)
        return {COUNTRY_ENAME: country.ename, COUNTRY_NAME: country.name}