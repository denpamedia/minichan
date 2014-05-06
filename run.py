#!/usr/bin/python3

from bottle import run
from app import app
from app.config import *

app.run(host=HOST, port=PORT)