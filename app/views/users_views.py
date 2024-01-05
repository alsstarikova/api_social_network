from app import app, USERS, models
from flask import request, Response, send_file
import json
from http import HTTPStatus
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

# Создаёт пользователя
@app.post('/user/create')
def user_create():
    try:
        # Распаковка json
        data = request.get_json()
        user_id = len(USERS)
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        # Проверка введённого email на валидность
        if not models.User.is_valid_email(email):
            return Response(
                json.dumps({"message": "Invalid inputs"}),
                HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )

        # Cоздание объекта типа user и сохранение его в базе данных
        user = models.User(user_id, first_name, last_name, email)
        USERS.append(user)

        # Создание соотвествующего ответа платформы на поступивший запрос
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

    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Invalid inputs"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

# Выдает данные по конкретному пользователю по его id
@app.get('/user/<int:user_id>')
def get_user(user_id):
    try:
        # Проверка на валидность введённого id
        if models.User.is_valid_id(user_id):
            return Response(
                json.dumps({"message": "User cannot be found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="application/json",
            )

        # Создание соотвествующего ответа платформы на поступивший запрос
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

    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Invalid inputs"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

# Выдает все посты пользователя, отсортированные по количеству реакций
@app.get('/users/<int:user_id>/posts')
def sorted_posts(user_id):
    try:
        # Проверка на валидность введённого id
        if models.User.is_valid_id(user_id):
            return Response(
                json.dumps({"message": "User cannot be found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="application/json",
            )

        # Распаковка json
        data = request.get_json()
        order = data['sort']
        if not(order=="asc" or order=="desc"):
            return Response(
                json.dumps({"message": "Invalid inputs"}),
                HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )

        # Сортировка постов пользователя
        user = USERS[user_id]
        sorted_posts = user.sort_posts(order)

        # Создание соотвествующего ответа платформы на поступивший запрос
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

    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Invalid inputs"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

# Генерирует список/график пользователей, отсортированный по количеству реакций
@app.get('/users/leaderboard')
def sorted_users():
    try:
        # Распаковка json
        data = request.get_json()
        type_of_request = data['type']

        # Генерация списка
        if type_of_request == "list":
            order = data['sort']
            sorted_users = []
            if order == "asc":
                sorted_users = sorted(USERS, key=lambda user: user.total_reactions)
            elif order == "desc":
                sorted_users = sorted(USERS, key=lambda user: user.total_reactions, reverse=True)
            else:
                return Response(
                    json.dumps({"message": "Invalid inputs"}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype="application/json",
                )

            # Создание соотвествующего ответа платформы на поступивший запрос
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

        # Генерация графика
        elif type_of_request == "graph":
            sorted_users = sorted(USERS, key=lambda user: user.total_reactions)
            user_names = [f'{user.first_name} {user.last_name}' for user in sorted_users]
            user_scores = [user.total_reactions for user in sorted_users]
            plt.bar(user_names, user_scores)
            plt.ylabel('User total reactions')
            plt.title('User leaderboard by amount of reactions')
            plt.savefig("app/users_leaderboard.png")

            # Создание соотвествующего ответа платформы на поступивший запрос
            return send_file("users_leaderboard.png")

        # Обработка неверно введённого типа для вывода отсортированных пользователей
        else:
            return Response(
                json.dumps({"message": "Invalid inputs"}),
                HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )

    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Invalid inputs"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )