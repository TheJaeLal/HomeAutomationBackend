
"""
Starts a Tornado static file server in a given directory.
To start the server in the current directory:
    tserv .
Then go to http://localhost:8000 to browse the directory.
Use the --prefix option to add a prefix to the served URL,
for example to match GitHub Pages' URL scheme:
    tserv . --prefix=jiffyclub
Then go to http://localhost:8000/jiffyclub/ to browse.
Use the --port option to change the port on which the server listens.
"""

from __future__ import print_function

import os
import sys
from argparse import ArgumentParser
import json
import time

from threading import Thread

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape


BASE = os.path.abspath(__file__)


class Worker(Thread):
    def __init__(self,path):
        super().__init__()
        self.path = path

    def run(self):
        while not os.path.exists(self.path):
            continue
        time.sleep(3)
        return

class Handler(object):
    def __init__(self):
        # self.BASE = os.abspath(__file__)
        pass
    def set_connection(self,conn):
        self.conn = conn
        return
    def write(self,message):
        self.conn.write_message(json.dumps(message))
        return
    def fetch_media(self,path):
        message = {'type':'Fetch','path':path}
        self.write(message)
        return

class Connection(tornado.websocket.WebSocketHandler):
    def initialize(self,handler):
        self.handler = handler
        pass

    def open(self):
        print("Opened")
        self.handler.set_connection(self)
        return

    def on_message(self,message):
        message_dict = eval(message)
        if message_dict['type'] == 'media':
            self.handler.media_list = message_dict
        else:

        print(message_dict)
        # self.write_message("Acknowledged!\n")
        # self.handler.server.write(message+"\n")
        # self.handler.server.finish()
        return

    def on_close(self):
        print("Closed")
        return

class FileHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        path = os.path.join(BASE,url_path)
        if not os.path.exists(path):
            handle.fetch_media(url_path)
            Worker(path).start()
            time.sleep(10)
        if not url_path or url_path.endswith('/'):
            url_path = url_path + 'index.html'
        return url_path   

class MediaServer(tornado.web.RequestHandler):
    def initialize(self,handler):
        self.handler = handler
        self.handler.server = self
        return
    @tornado.web.asynchronous
    def get(self):
        self.write(self.handler.media_list)
        self.finish()
        pass


class LightServer(tornado.web.RequestHandler):

    def initialize(self,handler):
        self.handler = handler
        self.handler.server = self
        return

    def get(self):
        self.write("HELLO\n")
        pass

    @tornado.web.asynchronous
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        # print data['light']
        # data = tornado.escape.json_encode(self.request.body.decode('utf-8'))
        print(type(data))
        data['type'] = 'light'
        self.handler.write(data)
        pass




def mkapp(prefix=''):
    global handle

    if prefix:
        path = '/' + prefix + '/(.*)'
    else:
        path = '/(.*)'

    handle = Handler()

    application = tornado.web.Application([
        ("/light",LightServer,{'handler':handle}),
        ("/connect",Connection,{'handler':handle}),
        ("/media",MediaServer,{'handler':handle}),
        (path, FileHandler, {'path': os.getcwd()}),
    ], debug=True)

    return application


def start_server(prefix='', port=8000):
    app = mkapp(prefix)
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()


def parse_args(args=None):
    parser = ArgumentParser(
        description=(
            'Start a Tornado server to serve static files out of a '
            'given directory and with a given prefix.'))
    parser.add_argument(
        '-f', '--prefix', type=str, default='',
        help='A prefix to add to the location from which pages are served.')
    parser.add_argument(
        '-p', '--port', type=int, default=8000,
        help='Port on which to run server.')
    parser.add_argument(
        'dir', help='Directory from which to serve files.')
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    os.chdir(args.dir)
    print('Starting server on port {}'.format(args.port))
    start_server(prefix=args.prefix, port=args.port)


if __name__ == '__main__':
    sys.exit(main())
