#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import http.server
import socketserver
import urllib.parse
import datetime

import process_added_cards
import generate_add_html

PORT = 10101

JPEG_NAME = 'jpegName'
START = 'date0F'
FINISH = 'date1F'
CITY = 'cityF'
POSITION = 'coordsF'
SENDERS = 'sendersF'
PARAMS = [JPEG_NAME, START, FINISH, CITY, POSITION, SENDERS]

JPEG_NAME_HEAD = 'C:\\fakepath\\'


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/add_card":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(generate_add_html.generate_add_html().encode())
            elif self.path.startswith('/add_card'):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                for p in PARAMS:
                    if p not in params:
                        self.wfile.write(('No param: ' + p).encode())
                        return
                jpegName = params[JPEG_NAME][0][len(JPEG_NAME_HEAD):]
                start = datetime.datetime.strptime(params[START][0], '%d.%m.%Y')
                finish = datetime.datetime.strptime(params[FINISH][0], '%d.%m.%Y')
                position = [float(x) for x in params[POSITION][0].split(';')]
                city = params[CITY][0]
                senders = params[SENDERS][0][:-1].split(',')
                ret = process_added_cards.process_added_card(jpegName, start, finish, position, city, senders)
                self.wfile.write(ret.encode())


        except Exception as ex:
            print('uups')
            print(ex)
            print(ex.args)


if __name__ == "__main__":
    try:
        httpd = socketserver.TCPServer(("", PORT), MyHandler)
        print("started httpserver at ", PORT)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C received, shutting down server")
        httpd.server_close()
