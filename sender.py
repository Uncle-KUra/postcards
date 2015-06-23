#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'


class Sender:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str({'name': self.name})
