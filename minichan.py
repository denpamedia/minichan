#!/usr/bin/env python3

from bottle import run, debug
from app import app
from app.config import *

if __name__ == '__main__':
	app.run(host=HOST, port=PORT, reloader=True, debug=True)
