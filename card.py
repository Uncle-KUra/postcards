#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import math
import datetime

DEG_2_RAD = math.pi / 180.0
EARTH_R = 6371110

HOME_LAT = 1.044593345
HOME_LONG = 0.527932341

SENDER_SELF = 'Юрий Курочкин'


class Card:
    def __init__(self, city, senders, sent, received, geo, file_name, add_time):
        self.city = city
        self.senders = senders
        self.start = sent
        self.finish = received
        self.position = geo
        self.file_name = file_name
        if add_time:
            self.add_time = add_time
        else:
            self.add_time = datetime.datetime.now()

    def __str__(self):
        return str({'city': str(self.city),
                    'senders': [str(x) for x in self.senders],
                    'start': self.start,
                    'finish': self.finish,
                    'position': self.position,
                    'file_name': self.file_name,
                    'add_time': self.add_time
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

    def rounded_distance_vk(self):
        print(self.distance())
        return str(round(self.distance() / 1e6, 1))

    def days(self):
        return (self.finish - self.start).days

    def days_vk(self):
        d = self.days()
        dh = d % 100
        dt = d % 10
        if 10 <= dh <= 20:
            return str(d) + ' дней'
        if dt == 1:
            return str(d) + ' день'
        if dt in [2, 3, 4]:
            return str(d) + ' дня'
        return str(d) + ' дней'

    def get_vk_description(self):
        s = '<br><br>'
        s += self.city.name + ', ' + self.city.country.name
        s += '<br>'
        s += self.start.date().strftime('%d.%m.%y')
        s += '<br>'
        s += 'Расстояние - ' + self.rounded_distance_vk() + ' Мм'
        s += '<br>'
        s += 'Время в пути - ' + self.days_vk()
        s += '<br>'
        if len(self.senders) == 1:
            if self.senders[0].name != SENDER_SELF:
                s += 'Отправитель - ' + self.senders[0].name
        else:
            s += 'Отправители - '
            s += ', '.join([x.name for x in self.senders[:-1]])
            s += ' и ' + self.senders[-1].name
        return s
