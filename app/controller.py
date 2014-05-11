from time import time
from datetime import datetime
import json

from mongoengine.context_managers import switch_db

from app import model
from app import config


def get_board_list():
    return json.dumps(config.BOARD_LIST)


def get_board(board):
    with switch_db(model.OriginalPost, board) as OriginalPost:
        thread_list = [dict(post.to_mongo()) for post in OriginalPost.get_all_reverse]
        for thread in thread_list:
            del thread['_id']
            del thread['_cls']

    return json.dumps({"board": board, "thread_list": thread_list})


def get_thread(board, thread):
    with switch_db(model.OriginalPost, board) as OriginalPost:
        original_post = OriginalPost.objects(post_id=thread)[0]
        original_post_dict = dict(original_post.to_mongo())

    with switch_db(model.ReplyPost, board) as ReplyPost:
        reply_list = [dict(reply.to_mongo()) for reply in ReplyPost.objects(original_post_link=original_post)]
        
    del original_post_dict['_id']
    del original_post_dict['_cls']

    for reply in reply_list:
        del reply['_id']
        del reply['_cls']
        del reply['original_post_link']

    return json.dumps({"board": board, "thread": thread, "original_post_dict": original_post_dict, "reply_list": reply_list})




def set_thread(board, subject, body):
    with switch_db(model.OriginalPost, board) as OriginalPost:
        creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        bump_time = time()
        post_id = next_counter(board=board)
        if OriginalPost.objects.count() >= config.NUMBER_OF_THREADS:
            OriginalPost.get_all[0].delete()
        OriginalPost(post_id=post_id, creation_time=creation_time, bump_time=bump_time, body=body, subject=subject).save()


def set_reply(board, thread, subject, body):
    creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    post_id = next_counter(board=board)

    with switch_db(model.OriginalPost, board) as OriginalPost:
        original_post = OriginalPost.objects(post_id=thread)[0]
        original_post.update(inc__bump_counter=1)

        if original_post.bump_counter >= config.BUMP_LIMIT:
            original_post.update(set__bump_limit=True)
        else:
            original_post.update(set__bump_time=time())

    with switch_db(model.ReplyPost, board) as ReplyPost:
        ReplyPost(creation_time=creation_time, post_id=post_id, body=body, subject=subject, original_post_link=original_post).save()



def next_counter(board):
    with switch_db(model.Counter, board) as Counter:
        Counter.objects(name='post_counter').update_one(inc__next_id=1)
    return [counter for counter in Counter.objects][0].next_id