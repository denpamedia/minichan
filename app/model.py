import time
import datetime

from mongoengine import *
from mongoengine.context_managers import switch_db


class Post(Document):
    '''Post superclass.

    '''

    post_id = LongField(required=True)
    subject = StringField(max_length=50)
    body = StringField(max_length=10000, required=True)
    creation_time = StringField(required=True)


    meta = {'allow_inheritance': True}


class OriginalPost(Post):
    '''Original Post class.
    bump_time is the time, when was posted last Reply for Original Post.
    bump_counter is the counter of Replies, that were posted on Thread.

    '''

    bump_time = FloatField(required=True)
    bump_counter = IntField(default=0, required=True)
    bump_limit = BooleanField(default=False)

    @queryset_manager
    def get_all(doc_cls, queryset):
        '''Method return list of Original Posts of board, sorted by bump time.'''
        return queryset.order_by('bump_time')

    @queryset_manager
    def get_all_reverse(doc_cls, queryset):
        '''Method return list of Original Posts of board, sorted by bump time reversed.'''
        return queryset.order_by('-bump_time')

    meta = {"db_alias": "b"}


class ReplyPost(Post):
    '''Field with link to OriginalPost instance.
    reverse_delete_rule=CASCADE means, that after deleting of Original Post,
    linked Reply Posts will be delete too.

    '''

    original_post_link = ReferenceField(OriginalPost, reverse_delete_rule=CASCADE)

    meta = {"db_alias": "b"}


class Counter(Document):
    name = StringField()
    next_id = IntField(default=0)

    meta = {"db_alias": "b"}