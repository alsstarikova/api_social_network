import re
import json

class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
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
class Post:
    def __init__(self, id, author_id, text):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = []
    def add_reaction(self, text):
        self.reactions.append(text)