import time

import tornado.web
import tornado.gen
import tornado.template

import app


class BoardHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        db = self.settings['db']
        data = yield db.messages.find({'post_type': 'thread'}).sort([('bump_time', -1)]).to_list(length=10)
        self.write(app.template_loader.load('board.html').generate(data=data))

    @tornado.gen.coroutine
    def post(self):
        db = self.settings['db']
        if (yield db.messages.find({'post_type': 'thread'}).count()) >= 2:
            to_delete = yield db.messages.find({'post_type': 'thread'}).sort([('bump_time', 1)]).to_list(length=1)
            yield db.messages.remove({'post_id': int(to_delete[0]['post_id'])})
            yield db.messages.remove({'thread_link': int(to_delete[0]['post_id'])})
        post_counter = (yield db.counters.find_one({'board_id': 'b'}))['counter']
        yield db.messages.insert({
            'post_type': 'thread',
            'post_id': post_counter,
            'subject': self.get_argument('subject'),
            'body': self.get_argument('body'),
            'creation_time': time.time(),
            'bump_time': time.time(),
            'bump_counter': 0,
            'bump_limit': False
            })
        yield db.counters.update({'board_id': 'b'}, {'$set': {'counter': post_counter + 1}})
        self.redirect('/')


class ThreadHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, thread_id):
        db = self.settings['db']
        if not (yield db.messages.find_one({'post_id': int(thread_id)})):
            raise tornado.web.HTTPError(404)
        data = {
        'original_post': (yield db.messages.find_one({'post_id': int(thread_id)})),
        'replies': (yield db.messages.find({'thread_link': int(thread_id)}).sort([('creation_time', 1)]).to_list(length=10))
        }
        self.write(app.template_loader.load('thread.html').generate(data=data))

    @tornado.gen.coroutine
    def post(self, thread_id):
        db = self.settings['db']
        if not (yield db.messages.find_one({'post_id': int(thread_id)})):
            raise tornado.web.HTTPError(404)
        post_counter = (yield db.counters.find_one({'board_id': 'b'}))['counter']
        yield db.messages.insert({
            'post_id': post_counter,
            'thread_link': int(thread_id),
            'subject': self.get_argument('subject'),
            'body': self.get_argument('body'),
            'creation_time': time.time(),
            })
        yield db.counters.update({'board_id': 'b'}, {'$inc': {'counter': 1}})
        yield db.messages.update({'post_id': int(thread_id)}, {'$inc': {'bump_counter': 1}})
        if (yield db.messages.find({'thread_link': int(thread_id)}).count()) >= 2:
            yield db.messages.update({'post_id': int(thread_id)}, {'$set': {'bump_limit': True}})
        else:
            yield db.messages.update({'post_id': int(thread_id)}, {'$set': {'bump_time': time.time()}})
        self.redirect('/{0}'.format(thread_id))