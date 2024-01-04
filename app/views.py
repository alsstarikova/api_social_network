from app import app, USERS, models, POSTS
from flask import request, Response, send_file
import json
from http import HTTPStatus
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

#todo: add try except
@app.route('/')
def index():
    return '<h1>Hello, world!</h1>'

@app.post('/user/create')
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.user_id,
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
            "id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.get_posts_information(),
        }),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response

@app.post('/posts/create')
def post_create():
    data = request.get_json()
    author_id = data["author_id"]
    text = data["text"]

    if author_id < 0 or author_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post_id = len(POSTS)
    post = models.Post(post_id, author_id, text)
    author = USERS[author_id]
    author.add_post(post)
    POSTS.append(post)
    response = Response(
        json.dumps({
            "id": post_id,
            "author_id": author_id,
            "text": text,
            "reactions": post.reactions,
        }),
        HTTPStatus.CREATED,
        mimetype = "application/json",
    )
    return response

@app.get('/posts/<int:post_id>')
def get_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    response = Response(
        json.dumps({
            "id": post_id,
            "author_id": post.author_id,
            "text": post.text,
            "reactions": post.reactions,
        }),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response

@app.post('/posts/<int:post_id>/reaction')
def add_reaction(post_id):
    if post_id < 0 or post_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]

    data = request.get_json()
    user_id = data['user_id']
    reaction = data['reaction']

    user = USERS[user_id]
    user.total_reactions += 1
    post.add_reaction(reaction)

    response = Response(status=HTTPStatus.OK)
    return response

@app.get('/users/<int:user_id>/posts')
def sorted_posts(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]

    data = request.get_json()
    order = data['sort']
    if not(order=="asc" or order=="desc"):
        return Response(status=HTTPStatus.BAD_REQUEST)
    sorted_posts = user.sort_posts(order)
    posts = [post.post_to_dict() for post in sorted_posts]
    response = Response(
        json.dumps(
            {
                "posts": posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
@app.get('/users/leaderboard')
def sorted_users():
    data = request.get_json()
    type_of_request = data['type']

    if type_of_request == "list":
        order = data['sort']
        sorted_users = []
        if order == "asc":
            sorted_users = sorted(USERS, key=lambda user: user.total_reactions)
        elif order == "desc":
            sorted_users = sorted(USERS, key=lambda user: user.total_reactions, reverse=True)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)
        users = [user.user_to_dict() for user in sorted_users]
        response = Response(
            json.dumps(
                {
                    "users": users,
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    elif type_of_request == "graph":
        sorted_users = sorted(USERS, key=lambda user: user.total_reactions)
        user_names = [f'{user.first_name} {user.last_name}' for user in sorted_users]
        user_scores = [user.total_reactions for user in sorted_users]
        plt.bar(user_names, user_scores)
        plt.ylabel('User total reactions')
        plt.title('User leaderboard by amount of reactions')
        plt.savefig("app/users_leaderboard.png")
        return send_file("users_leaderboard.png")