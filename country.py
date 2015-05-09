#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'


class Country:
    def __init__(self, ename, name):
        self.ename = ename
        self.name = name

    def __str__(self):
        return str({'ename': self.ename, 'name': self.name})