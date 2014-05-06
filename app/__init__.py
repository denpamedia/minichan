from bottle import Bottle

from app.config import *
from app.model import *


# Connect to board's DBs
for board in BOARD_LIST:
    register_connection(board, board)


# Make or connect post counters for each board
for board in BOARD_LIST:
    with switch_db(Counter, board) as myCounter:
        myCounter(name='post_counter').save()


app = Bottle()


from app import view