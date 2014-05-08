#!/usr/local/bin/python3

from bottle import run
from app import app
from app.config import *

if __name__ == '__main__':
	app.run(host=HOST, port=PORT)
