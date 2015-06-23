#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'


class Country:
    def __init__(self, ename, name):
        self.ename = ename
        self.name = name
        self.city_list = list()

    def __str__(self):
        return str({'ename': self.ename, 'name': self.name})

    def add_city(self, city):
        self.city_list.append(city)
