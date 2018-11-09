from flask import Flask, g

import os
import login
import tabledb

app = Flask(__name__)

app.add_url_rule("/", "home", login.home, methods=['GET', 'POST'])
app.add_url_rule("/login", "login", login.login, methods=['GET', 'POST'])
app.add_url_rule("/logout", "logout", login.logout, methods=['GET', 'POST'])
app.add_url_rule("/user/<username>", 'user', login.user, methods=['GET', 'POST'])


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
