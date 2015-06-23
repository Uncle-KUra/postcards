#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import argparse
import json
from postcards_db import DB


def do_import_senders(file_name):
    with DB() as db:
        for card_info in json.load(open(file_name)):
            for sender in card_info['senders']:
                if not db.find_sender(sender):
                    db.add_sender(sender)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("old_file", help="file with old senders json ")
    params = parser.parse_args()
    do_import_senders(params.old_file)

