from flask import Flask, g
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room

import os
import login
import tabledb
import multistream
import random as rnd
import time

app = Flask(__name__)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

# socket io
socketio = SocketIO(app)

# chat room variables
list_of_rooms = []
dict_users = {}
user_sdp = {}
user_ice = {}

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



# @socketio.on('client description', namespace='/video')
@socketio.on('sdp description')
def client_description(json):
    # global list_of_rooms
    # global dict_users

    # room = rnd.randint(0, 10000)
    # while room in list_of_rooms:
    #     room = rnd.randint(0, 10000)
    #
    # join_room(room)
    # list_of_rooms.append(room)
    # room = int(json['rid'])
    room = int(json['rid'])
    username = json['uuid']
    new_user = json['new_user']
    # dict_users[room] = [username]
    # user_sdp[username] = json
    # print(json['uuid'])
    # socketio.emit('peer connect', json, broadcast=True)
    # socketio.emit('peer connect', json, room=room, broadcast=True)
    # socketio.emit('room id', {'data': room}, room=room)
    # print(dict_users[room])
    # print(list_of_rooms)
    # if room == -1:
    #     print('Incorrect User: ' + username)

    # for u in dict_users[room]:
    #     if u in user_sdp.keys():
    #         socketio.emit('set remote', user_sdp[u], room=room, broadcast=True)
    json['rid'] = room
    socketio.emit('set remote', json, room=room, broadcast=True)



@socketio.on('create room')
def create_room(json):
    room = rnd.randint(0, 10000)
    while room in list_of_rooms:
        room = rnd.randint(0, 10000)

    join_room(room)
    list_of_rooms.append(room)
    username = json['uuid']
    dict_users[room] = [username]
    socketio.emit('room id', {'data': room}, room=room)


@socketio.on('join')
def room_join(json):
    # global list_of_rooms
    # global dict_users

    room = int(json['rid'])

    if room not in list_of_rooms:
        print('Why are we here')
        return

    user = json['uuid']
    if user in dict_users[room]:
        print('Why are we here 2')
        return
        # dict_users[room].append(user)
        # join_room(room)

    # for u in dict_users[room]:
    socketio.emit('create offer', {'new_user': user}, room=room, broadcast=True)
    dict_users[room].append(user)
    join_room(room)

    # print(dict_users[room])
    # for u in dict_users[room]:
    #     if u in user_sdp.keys():
    #         socketio.emit('set remote', user_sdp[u], room=room, broadcast=True)

    # time.sleep(0.5)
    # for u in dict_users[room]:
    #     if u in user_ice.keys():
    #         socketio.emit('peer connect', user_ice[u], room=room, broadcast=True)


@socketio.on('ice candidate')
# @socketio.on('ice candidate', namespace='/video')
def ice_candidate(json):
    room = int(json['rid'])
    username = json['uuid']
    # user_ice[username] = json

    if room not in list_of_rooms:
        return

    if username not in dict_users[room]:
        return

    # user = json['uuid']
    # if user not in dict_users[room]:
    #     dict_users.append(user)
    #     join_room(room)

    # socketio.emit('peer connect', json, broadcast=True)
    json['rid'] = room
    socketio.emit('ice connect', json, room=room, broadcast=True)


@socketio.on('leave room')
def room_leave(json):
	room = int(json['rid'])
	dict_users[room].remove(json['uuid'])
	leave_room(room)
	if len(dict_users[room]) == 0:
		print(list_of_rooms)
		print(dict_users)
		dict_users.pop(room)
		list_of_rooms.remove(room)
		print(list_of_rooms)

	socketio.emit('left room', json, room=room, broadcast=True)



app.secret_key = os.urandom(12)
if __name__ == "__main__":
    # app.run(host='0.0.0.0', threaded=True)
    socketio.run(app)
