#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import argparse
import json
import datetime
import os
from postcards_db import DB

CARDS_PATH = "~/Downloads/Cards/"

def process_added_card(jpegName, start, finish, position, city, senders):
    print(jpegName)
    print(start)
    print(finish)
    print(position)
    print(city)
    print(senders)