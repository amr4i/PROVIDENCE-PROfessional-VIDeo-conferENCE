from flask import Flask, g
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room

import os
import login
import tabledb
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


@login_manager.user_loader
def load_user(user_id):
    user = login.User(user_id)
    return user


@socketio.on('check connect')
def test_video_feed(msg):
    print('*'*45)
    print(str(msg))
    print('*'*45)


@socketio.on('sdp description')
def client_description(json):
    room = int(json['rid'])
    username = json['uuid']
    new_user = json['new_user']

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

    room = int(json['rid'])

    if room not in list_of_rooms:
        # alert("No such room exists!")
        socketio.emit('restore state notInRoom', {"type":"alert", "msg":"Room "+str(room)+" does not exist!"})
        return

    user = json['uuid']
    if user in dict_users[room]:
        # print('Why are we here 2')
        socketio.emit('restore state notInRoom', {"type":"alert", "msg":"User "+str(user)+" already exists in room " + str(room) + "!"})
        return

    socketio.emit('create offer', {'new_user': user}, room=room, broadcast=True)
    dict_users[room].append(user)
    join_room(room)



@socketio.on('ice candidate')
def ice_candidate(json):
    room = int(json['rid'])
    username = json['uuid']

    if room not in list_of_rooms:
        socketio.emit('restore state notInRoom', {"type":"alert", "msg":"Room "+str(room)+" does not exist!"})
        return

    if username not in dict_users[room]:
        socketio.emit('restore state notInRoom', {"type":"alert", "msg":"Encountered Unexpected ICE candidate. Please Re-join!"})
        return

    json['rid'] = room
    socketio.emit('ice connect', json, room=room, broadcast=True)


@socketio.on('leave room')
def room_leave(json):
	room = int(json['rid'])
	dict_users[room].remove(json['uuid'])
	leave_room(room)
	if len(dict_users[room]) == 0:
		dict_users.pop(room)
		list_of_rooms.remove(room)

	socketio.emit('left room', json, room=room, broadcast=True)



app.secret_key = os.urandom(12)
if __name__ == "__main__":
    socketio.run(app)
