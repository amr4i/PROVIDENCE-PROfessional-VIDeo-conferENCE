from flask import Flask, g
from flask_login import LoginManager
from flask_socketio import SocketIO

import os
import login
import tabledb
import multistream

app = Flask(__name__)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

# socket io
socketio = SocketIO(app)

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


@socketio.on('check connect')
# @socketio.on('check connect', namespace='/video')
def test_video_feed(msg):
    print('*'*45)
    print(str(msg))
    print('*'*45)
    # return multistream.check_connect(msg)


# @socketio.on('connect', namespace='/video')
# def test_video_feed(msg):
#     print('*'*45)
#     print(str(msg))
#     print('*'*45)


# @socketio.on('client description', namespace='/video')
@socketio.on('client description')
def test_video_feed(json):
    print('client')
    # print('*'*45)
    # print(str(json))
    # print('*'*45)
    socketio.emit('peer connect', json, broadcast=True)


@socketio.on('ice candidate')
# @socketio.on('ice candidate', namespace='/video')
def test_video_feed(json):
    # print('ice')
    # print('*'*45)
    # print(str(json))
    # print('*'*45)
    socketio.emit('peer connect', json, broadcast=True)



app.secret_key = os.urandom(12)
if __name__ == "__main__":
    # app.run(host='0.0.0.0', threaded=True)
    socketio.run(app)
