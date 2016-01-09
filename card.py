#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import math

DEG_2_RAD = math.pi / 180.0
EARTH_R = 6371110

HOME_LAT = 1.044593345
HOME_LONG = 0.527932341


class Card:
    def __init__(self, city, senders, sent, received, geo):
        self.city = city
        self.senders = senders
        self.start = sent
        self.finish = received
        self.position = geo

    def __str__(self):
        return str({'city': str(self.city),
                    'senders': [str(x) for x in self.senders],
                    'start': self.start,
                    'finish': self.finish,
                    'position': self.position
        })

    def weeks(self):
        return math.ceil((self.finish - self.start).days / 7)

    def distance(self):
        lat = DEG_2_RAD * self.position[0]
        long = DEG_2_RAD * self.position[1]
        return EARTH_R * math.acos(math.sin(HOME_LAT) * math.sin(lat)
                                   + math.cos(HOME_LAT) * math.cos(lat) * math.cos(HOME_LONG - long))

    def rounded_distance(self):
        return int(round(self.distance() / 1e6, 0))

