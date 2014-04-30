from mongoengine import *
from mongoengine.context_managers import switch_db
from config import *

# Post superclass
class Post(Document):
	subject = StringField(max_length=50)
	body = StringField(max_length=3000, required=True)
	creation_time = StringField()
	post_id = LongField()
	meta = {'allow_inheritance': True}

class Thread(Post):
	bump_time = FloatField()
	bump_counter = IntField(default=0)
	@queryset_manager
	def objects(doc_cls, queryset):
		return queryset.order_by('-bump_time')
	meta = {"db_alias": "b"}

class Reply(Post):
	op_link = IntField()
	meta = {"db_alias": "b"}

class Counter(Document):
	name = StringField()
	last_id = IntField(default=0)
	meta = {"db_alias": "b"}

# Connect to board's DBs
for board in board_list:
	register_connection(board, board)

# Make post counters to each board
for board in board_list:
	with switch_db(Counter, board) as myCounter:
		myCounter(name='post_counter').save()
