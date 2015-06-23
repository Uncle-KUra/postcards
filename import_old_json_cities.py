#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import argparse
import json
from postcards_db import DB


def do_import_country(file_name):
    with DB() as db:
        for new_city in json.load(open(file_name)):
            city = db.find_city(new_city["ename"])
            if city is not None:
                print("Found ", city, " for ", new_city)
            else:
                country = db.find_country_by_name(new_city["country"])
                if country is None:
                    print("Country missing! for ", new_city)
                else:
                    db.add_city(new_city["ename"], new_city["name"], country)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("old_file", help="file with old country json ")
    params = parser.parse_args()
    do_import_country(params.old_file)
