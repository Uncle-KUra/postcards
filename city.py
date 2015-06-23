#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'


class City:
    def __init__(self, ename, name, country):
        self.ename = ename
        self.name = name
        self.country = country

    def __str__(self):
        return str({'ename': self.ename, 'name': self.name, 'country': self.country.ename})
