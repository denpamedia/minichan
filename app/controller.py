from time import time
from datetime import datetime
import hashlib

from app import model
from app import config


def get_board():
    return model.Thread.all_threads


def get_thread(thread_id):
    return {
    "original_post": dict(model.Thread.objects(post_id=thread_id)[0].to_mongo()),
    "reply_list": [dict(reply.to_mongo()) for reply in model.Reply.all(thread_link=model.Thread.objects(post_id=thread_id)[0])]
    }


def make_new_thread(subject, body, image):
    if model.Thread.objects.count() >= config.NUMBER_OF_THREADS:
        model.Thread.oldest.delete()

    img = model.Image()
    img.img_src.put(image)
    img.img_id = str(hashlib.md5(img.img_src.read()).hexdigest())

    original_post = model.Thread()
    original_post.post_id = next_counter()
    original_post.creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    original_post.body = body
    original_post.subject = subject
    original_post.image_uri = '/image/{0}'.format(img.img_id)
    original_post.thumb_uri = '/thumb/{0}'.format(img.img_id)
    original_post.last_bump_time = time()
    original_post.save()

    img.post_link = original_post
    img.save()


def make_new_reply(thread_id, image, body):
    original_post = model.Thread.objects(post_id=thread_id)[0]
    original_post.update(inc__bump_counter=1)

    if original_post.bump_counter >= config.BUMP_LIMIT:
        original_post.update(set__bump_limit=True)
    else:
        original_post.update(set__last_bump_time=time())

    img = model.Image()
    img.img_src.put(image)
    img.img_id = str(hashlib.md5(img.img_src.read()).hexdigest())

    reply_post = model.Reply()
    reply_post.post_id = next_counter()
    reply_post.creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    reply_post.body = body
    reply_post.image_uri = '/image/{0}'.format(img.img_id)
    reply_post.thumb_uri = '/thumb/{0}'.format(img.img_id)
    reply_post.thread_link = original_post
    reply_post.save()

    img.post_link = reply_post
    img.save()


def next_counter():
    model.Counter.objects(name='post_counter').update_one(inc__next_id=1)
    return model.Counter.objects[0].next_id