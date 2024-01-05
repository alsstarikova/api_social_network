import re
import json
from app import USERS, POSTS

# Класс для создания пользователей
class User:
    # Инициализация пользователя
    def __init__(self, user_id, first_name, last_name, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []

    # Проверка на валидность email
    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    # Проверка на валидность id
    @staticmethod
    def is_valid_id(user_id):
        return (user_id < 0 or user_id >= len(USERS))

    # Добавление поста
    def add_post(self, post):
        self.posts.append(post)

    # Получение информации о постах пользователя
    def get_posts_information(self):
        return json.dumps({
            "number": len(self.posts),
        })

    # Сортировка постов
    def sort_posts(self, order):
        posts = sorted(self.posts, key=lambda post: post.get_total_count_of_reactions())
        if order == "asc":
            return posts
        return posts[::-1]

    # Создание словаря, отображающего всю информацию о пользователе
    def user_to_dict(self):
        return dict({
            "id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
        })

    # Отображение информации о пользователе на главной странице
    def repr(self):
        return f"{self.user_id}. {self.first_name} {self.last_name}"

# Класс для создания постов
class Post:
    # Инициализация поста
    def __init__(self, post_id, author_id, text):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    # Проверка на валидность id
    @staticmethod
    def is_valid_id(post_id):
        return (post_id < 0 or post_id >= len(POSTS))

    # Добавление поста
    def add_reaction(self, text):
        self.reactions.append(text)

    # Получение информации о количестве реакций
    def get_total_count_of_reactions(self):
        return len(self.reactions)

    # Создание словаря, отображающего всю информацию о посте
    def post_to_dict(self):
        return dict({
            "post_id": self.post_id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
        })

    # Отображение информации о посте на главной странице
    def repr(self):
        return f"{self.post_id}. {self.author_id} {self.text}"