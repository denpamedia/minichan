from mongoengine import *


class Post(Document):
    post_id = LongField(required=True)
    creation_time = StringField(required=True)
    body = StringField(max_length=6000, required=True)
    image_uri = StringField()
    thumb_uri = StringField()

    meta = {'allow_inheritance': True}


class Thread(Post):
    last_bump_time = IntField(required=True)
    bump_counter = IntField(default=0, required=True)
    bump_limit = BooleanField(default=False, required=True)

    @queryset_manager
    def all(doc_cls, queryset):
        return [dict(x.to_mongo()) for x in queryset.order_by('-last_bump_time').only('post_id', 'creation_time',
            'body', 'image_uri', 'thumb_uri', 'last_bump_time', 'bump_counter', 'bump_limit')]

    @queryset_manager
    def oldest(doc_cls, queryset):
        return queryset.order_by('last_bump_time')[0]


class Reply(Post):
    thread_link = ReferenceField(Thread, reverse_delete_rule=CASCADE, required=True)

    @queryset_manager
    def all(doc_cls, queryset):
        return queryset.order_by('creation_time').only('post_id', 'creation_time',
            'body', 'image_uri', 'thumb_uri')


class Image(Document):
    img_id = StringField(required=True)
    img_src = ImageField(thumbnail_size=(300, 250, True), required=True)
    post_link = ReferenceField(Post, reverse_delete_rule=CASCADE, required=True)


class Counter(Document):
    name = StringField()
    next_id = IntField(default=0)
