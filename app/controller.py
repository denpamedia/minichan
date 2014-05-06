from time import time
from datetime import datetime

from mongoengine.context_managers import switch_db

from app import model
from app import config


def get_original_posts_iter(board):
    '''switch_db switch Board DataBase.
    Function return iterator for Original Posts of Board.

    '''

    with switch_db(model.OriginalPost, board) as OriginalPost:
        return (original_post for original_post in OriginalPost.objects())


def get_reply_posts_iter(board, original_post_id):
    '''Return Original Post of thread and iterator for Reply Posts of thread.

    '''

    with switch_db(model.OriginalPost, board) as OriginalPost:
        original_post = OriginalPost.objects(post_id=original_post_id)[0]

    with switch_db(model.ReplyPost, board) as ReplyPost:
        return (reply_post for reply_post in ReplyPost.objects(original_post_link=original_post))


def get_original_post(board, original_post_id):
    '''Return Original Post of thread.

    '''

    with switch_db(model.OriginalPost, board) as OriginalPost:
        return OriginalPost.objects(post_id=original_post_id)[0]


def set_original_post(board, subject, body):
    '''Make and save new Original Post instance.

    '''

    creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    bump_time = time()
    post_id = next_counter(board=board)

    with switch_db(model.OriginalPost, board) as OriginalPost:
        if OriginalPost.objects.count() >= config.NUMBER_OF_THREADS:
            [post for post in OriginalPost.objects][-1].delete()
        OriginalPost(post_id=post_id, creation_time=creation_time, bump_time=bump_time, body=body, subject=subject).save()


def set_reply_post(board, original_post_id, subject, body):
    '''Make and save new Reply Post instance.

    '''

    creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    post_id = next_counter(board=board)

    with switch_db(model.OriginalPost, board) as OriginalPost:
        original_post = OriginalPost.objects(post_id=original_post_id)[0]

    with switch_db(model.ReplyPost, board) as ReplyPost:
        ReplyPost(creation_time=creation_time, post_id=post_id, body=body, subject=subject, original_post_link=original_post).save()
        if ReplyPost.objects(original_post_link=original_post).count() <= config.BUMP_LIMIT:
            bump_thread(board=board, original_post_id=original_post_id)



def next_counter(board):
    '''Increment Board's Post Counter,
    and return it's value.

    '''

    with switch_db(model.Counter, board) as Counter:
        Counter.objects(name='post_counter').update_one(inc__next_id=1)
        return [counter for counter in Counter.objects][0].next_id


def bump_thread(board, original_post_id):
    '''Increment Bump Counter of Original Post,
    and update it's bump time field.

    '''

    with switch_db(model.OriginalPost, board) as OriginalPost:
        OriginalPost.objects(post_id=original_post_id).update_one(inc__bump_counter=1)
        OriginalPost.objects(post_id=original_post_id).update_one(set__bump_time=time())
