from flask import Flask
from mongoengine import *

from app.config import *
from app.model import *


connect("b_test")

Counter(name='post_counter').save()

minichan = Flask(__name__)

import app.view