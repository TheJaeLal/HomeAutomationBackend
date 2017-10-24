
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

import tornado.ioloop
import tornado.web
import tornado.websocket


class FileHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path = url_path + 'index.html'
        return url_path

class Handler(object):
    def __init__(self):
        pass
    def set_connection(self,conn):
        self.conn = conn
        return
    def write(self,message):
        self.conn.write_message(message)
        return

class Server(tornado.web.RequestHandler):

    def initialize(self,handler):
        self.handler = handler
        self.handler.server = self
        return

    def get(self):
        self.write("HELLO\n")
        pass

    @tornado.web.asynchronous
    def post(self):
        # data = tornado.escape.json_decode(self.request.body)
        # print data['light']
        data = self.request.body
        self.handler.write(data)


class Connection(tornado.websocket.WebSocketHandler):
    def initialize(self,handler):
        self.handler = handler
        pass

    def open(self):
        print("Opened")
        self.handler.set_connection(self)
        return

    def on_message(self,message):
        print(message)
        # self.write_message("Acknowledged!\n")
        self.handler.server.write(message+"\n")
        self.handler.server.finish()
        return

    def on_close(self):
        print("Closed")
        return

def mkapp(prefix=''):
    if prefix:
        path = '/' + prefix + '/(.*)'
    else:
        path = '/(.*)'

    handle = Handler()

    application = tornado.web.Application([
        ("/light",Server,{'handler':handle}),
        ("/connect",Connection,{'handler':handle}),
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
