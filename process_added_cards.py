#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import argparse
import json
import datetime
import os
import os.path
import math
import shutil

from gi.repository import GExiv2

from postcards_db import DB

CARDS_PATH = '/home/yurakura/Downloads/Cards/'


def process_added_card(jpeg_name, start, finish, position, city, senders):
    if not os.path.isfile(CARDS_PATH + jpeg_name):
        return 'File not found: ' + CARDS_PATH + jpeg_name

    with DB() as db:
        db_senders = list()
        for name in senders:
            db_sender = db.find_sender(name)
            if not db_sender:
                return 'Sender not found: ' + name
            if not db_sender.ename:
                return 'Sender has no ename: ' + name
            db_senders.append(db_sender)
        db_city = db.find_city_by_name(city)
        if len(db_city) != 1:
            return 'City not found: ' + city
        db_city = db_city[0]
        if not db_city.country.tld:
            return 'Country has no tld: ' + city

        db_card = db.add_card(db_city, db_senders, start, finish, position)

        tags = [str(start.year)]
        weeks = db_card.weeks()
        if weeks == 1:
            tags.append('1_week')
        else:
            tags.append(str(weeks) + '_weeks')
        tags.append('Country_' + db_city.country.tld)
        for db_sender in db_senders:
            tags.append(('Sender ' + db_sender.ename).replace(' ', '_'))
        tags.append('Distance_' + str(db_card.rounded_distance()) + '_Mm')

        new_name = start.date().strftime('%Y%m%d') + '-' + db_city.country.ename + '-' + db_city.ename
        while os.path.isfile(CARDS_PATH + new_name):
            new_name += '_X'

        shutil.copyfile(CARDS_PATH + jpeg_name, CARDS_PATH + new_name)

        exif = GExiv2.Metadata(CARDS_PATH + new_name)
        # longitude, latitude, altitude
        exif.set_gps_info(position[0], position[1], 0)
        IPTC = 'Iptc.Application2.'
        exif[IPTC + 'City'] = db_city.ename
        exif[IPTC + 'CountryName'] = db_city.country.ename
        exif[IPTC + 'Keywords'] = ', '.join(tags)
        exif[IPTC + 'Subject'] = ', '.join(tags)

        exif.save_file()
        return str(new_name)
