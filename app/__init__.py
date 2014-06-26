import tornado.web
import motor
import pymongo
import tornado.template

import app.handlers


with pymongo.MongoClient() as client:
    db = client.test
    counters = db.counters
    if not counters.find_one({'board_id': 'b'}):
        counters.insert({'board_id': 'b', 'counter': 1})


db = motor.MotorClient().test

template_loader = tornado.template.Loader('app/templates')


minichan = tornado.web.Application(
    [
        (r'/', app.handlers.BoardHandler),
        (r'/([0-9]+)', app.handlers.ThreadHandler)
    ],
    db=db,
    static_path='app/static',
    debug=True
)