from app import app, USERS, models, POSTS
from flask import request, Response
import json
from http import HTTPStatus

# Создаёт пост
@app.post('/posts/create')
def post_create():
    try:
        # Распаковка json
        data = request.get_json()
        author_id = data["author_id"]
        text = data["text"]

        # Проверка на валидность введённого id
        if models.User.is_valid_id(author_id):
            return Response(
                json.dumps({"message": "Author cannot be found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="application/json",
            )

        # Cоздание объекта типа post и сохранение его в базе данных
        post_id = len(POSTS)
        post = models.Post(post_id, author_id, text)
        author = USERS[author_id]
        author.add_post(post)
        POSTS.append(post)

        # Создание соотвествующего ответа платформы на поступивший запрос
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

    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Invalid inputs"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

# Выдает данные по конкретному посту по его id
@app.get('/posts/<int:post_id>')
def get_post(post_id):
    try:
        # Проверка на валидность введённого id
        if models.Post.is_valid_id(post_id):
            return Response(
                json.dumps({"message": "Post cannot be found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="application/json",
            )

        # Создание соотвествующего ответа платформы на поступивший запрос
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

    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Invalid inputs"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

# Пользователь ставит реакцию на конкретный пост
@app.post('/posts/<int:post_id>/reaction')
def add_reaction(post_id):
    try:
        # Проверка на валидность введённого id
        if models.Post.is_valid_id(post_id):
            return Response(
                json.dumps({"message": "Post cannot be found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="application/json",
            )

        # Распаковка json
        data = request.get_json()
        user_id = data['user_id']
        reaction = data['reaction']

        # Добавление реакции и обновление соответсвующих переменных
        # у пользователя и поста
        post = POSTS[post_id]
        user = USERS[user_id]
        user.total_reactions += 1
        post.add_reaction(reaction)

        # Создание соотвествующего ответа платформы на поступивший запрос
        response = Response(status=HTTPStatus.OK)
        return response

    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Invalid inputs"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
