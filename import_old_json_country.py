#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import argparse
import json
from postcards_db import DB


def do_import_country(file_name):
    with DB() as db:
        for new_country in json.load(open(file_name)):
            country = db.find_country_by_name(new_country["name"])
            if country is not None:
                print("Found ", country, " for ", new_country)
            else:
                db.add_country(new_country["ename"], new_country["name"], '')
                pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("old_file", help="file with old country json ")
    params = parser.parse_args()
    do_import_country(params.old_file)
