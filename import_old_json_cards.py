#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import argparse
import json
import datetime
from postcards_db import DB


def do_import_cards(file_name):
    with DB() as db:
        for card in json.load(open(file_name)):
            senders = [x for x in card['senders'] if not db.find_sender(x)]
            if senders:
                print('No senders: ', senders)
                continue
            senders = [db.find_sender(x) for x in card['senders']]
            city = db.find_city_by_name(card['city'])
            if not city or len(city) != 1:
                print('No city: ', card['city'])
                continue
            city = city[0]
            sent = datetime.date(card['send'][0], card['send'][1], card['send'][2])
            received = datetime.date(card['receive'][0], card['receive'][1], card['receive'][2])
            geo = card['geo']
            db.add_card(city, senders, sent, received, geo)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("old_file", help="file with old json ")
    params = parser.parse_args()
    do_import_cards(params.old_file)
