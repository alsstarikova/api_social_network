from app import app, USERS, POSTS

# Отображает сообщение на домашней странице
@app.route('/')
def index():
    response = (
        f"<h1>Hello, world!</h1>"
        f"<h3>USERS:</h3><br> {'<br>'.join([user.repr() for user in USERS])}<br><br>"
        f"<h3>POSTS:</h3><br> {'<br>'.join([post.repr() for post in POSTS])}<br>"
    )
    return response
