#!/usr/bin/env python3

import tornado.ioloop

from app import minichan


print('Listening on http://localhost:8888')
minichan.listen(8888)
tornado.ioloop.IOLoop.instance().start()