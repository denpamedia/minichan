from mongoengine import *


class Post(Document):
    post_id = LongField(required=True)
    creation_time = StringField(required=True)
    body = StringField(required=True, max_length=6000)
    subject = StringField()
    image_id = StringField()

    meta = {'allow_inheritance': True}


class Thread(Post):
    bump_time = FloatField(required=True)
    bump_counter = IntField(required=True, default=0)
    bump_limit = BooleanField(required=True, default=False)
    @queryset_manager
    def all(doc_cls, queryset):
        return [dict(x.to_mongo()) for x in queryset.order_by('-bump_time').only('post_id', 'creation_time',
            'body', 'image_id', 'subject', 'bump_time', 'bump_counter', 'bump_limit')]
    @queryset_manager
    def oldest(doc_cls, queryset):
        return queryset.order_by('bump_time')[0]


class Reply(Post):
    thread_link = ReferenceField(Thread, reverse_delete_rule=CASCADE, required=True)
    @queryset_manager
    def all(doc_cls, queryset):
        return queryset.order_by('creation_time').only('post_id', 'creation_time',
            'body', 'image_id')


class Image(Document):
    img_id = StringField(required=True)
    img_src = ImageField(thumbnail_size=(300, 250, True), required=True)
    post_link = ReferenceField(Post, reverse_delete_rule=CASCADE, required=True)


class Counter(Document):
    name = StringField()
    next_id = IntField(default=0)


def next_counter():
    Counter.objects(name='post_counter').update_one(inc__next_id=1)
    return Counter.objects[0].next_id