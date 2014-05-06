#!/usr/bin/python3

from bottle import run
from app import app

app.run(host='localhost', port=8080, debug=True, reloader=True)
