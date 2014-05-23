from json import loads

from flask import Flask
from mongoengine import *

from app.config import *
from app.model import *


connect("b_test")

Counter(name='post_counter').save()

minichan = Flask(__name__)

minichan.jinja_env.globals.update(loads=loads)

import app.view