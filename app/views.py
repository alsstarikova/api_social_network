from app import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.route('/')
def index():
    return '<h1>Hello, world!</h1>'

@app.post('/user/create')
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.posts,
        }),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response

@app.get('/user/<int:user_id>')
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.posts,
        }),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response