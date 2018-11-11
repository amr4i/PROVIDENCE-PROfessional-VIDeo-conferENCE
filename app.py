from flask import Flask, g
from flask_login import LoginManager

import os
import login
import tabledb
import multistream

app = Flask(__name__)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

app.add_url_rule("/", "home", login.home, methods=['GET', 'POST'])
app.add_url_rule("/login", "login", login.login, methods=['GET', 'POST'])
app.add_url_rule("/logout", "logout", login.logout, methods=['GET', 'POST'])
app.add_url_rule("/user/<username>", 'user', login.user, methods=['GET', 'POST'])
app.add_url_rule("/video_feed", 'video_feed', multistream.video_feed, methods=['GET', 'POST'])


@login_manager.user_loader
def load_user(user_id):
    user = login.User(user_id)
    # user.id = user_id
    return user


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
