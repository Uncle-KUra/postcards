#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import argparse
import json
import datetime
import os
from gi.repository import GExiv2

from postcards_db import DB

CARDS_PATH = "~/Downloads/Cards/"

def process_added_card(jpbegName, start, finish, position, city, senders):



    exif = GExiv2.Metadata('riga.jpg')
    # longitude, latitude, altitude
    exif.set_gps_info(position[0], position[1], 0)
    IPTC = 'Iptc.Application2.'
    exif[IPTC + 'City'] = 'Toronto'
    exif[IPTC + 'ProvinceState'] = 'Ontario'
    exif[IPTC + 'CountryName'] = 'Canada'

    exif.save_file()

    with DB() as db:
        db_senders = list()
        for name in senders:
            db_sender = db.find_sender(name)
            if not db_sender:
                return "Sender not found: " + name
            db_senders.append(db_sender)
        db_city = db.find_city_by_name(city)
        if not db_city:
            return "Sender not found: " + name






        db.add_card(db_city, db_senders, start, finish, position)
