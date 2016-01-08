#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'


class Sender:
    def __init__(self, name, ename):
        self.name = name
        self.ename = ename
        self.card_list = list()

    def __str__(self):
        return str({'name': self.name, 'ename': self.ename})

    def add_card(self, card):
        self.card_list.append(card)

