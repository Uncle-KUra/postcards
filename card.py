#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import math

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
        return 123.4456

    def rounded_distance(self):
        return round(self.distance(), 0)
