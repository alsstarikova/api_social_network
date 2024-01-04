import re
import json

class User:
    def __init__(self, user_id, first_name, last_name, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False
    def add_post(self, post):
        self.posts.append(post)
    def get_posts_information(self):
        return json.dumps({
            "number": len(self.posts),
        })
    def sort_posts(self, order):
        posts = sorted(self.posts, key=lambda post: post.get_total_count_of_reactions())
        if order == "asc":
            return posts
        return posts[::-1]
    def user_to_dict(self):
        return dict({
            "id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
        })
    def __lt__(self, other):
        return self.total_reactions < other.total_reactions

class Post:
    def __init__(self, post_id, author_id, text):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []
    def add_reaction(self, text):
        self.reactions.append(text)
    def get_total_count_of_reactions(self):
        return len(self.reactions)
    def post_to_dict(self):
        return dict({
            "post_id": self.post_id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
        })

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__