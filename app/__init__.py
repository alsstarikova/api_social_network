from flask import Flask

app = Flask(__name__)

USERS = [] # list for objects of type User
POSTS = [] # list for objects of type Post

from app import views_all
from app import models
from app import views