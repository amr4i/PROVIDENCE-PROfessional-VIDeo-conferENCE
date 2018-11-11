import os
import tabledb

from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from functools import wraps
from flask_login import UserMixin, login_required, login_user, logout_user, \
    current_user


class User():
    def __init__(self, name=''):
        self.username = name
        self.authenticated = False

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


def login():
    # print('*\n'*10)
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    # print(username)
    # print(password)

    user_db = tabledb.db_session()

    query = user_db.query(tabledb.UserBase).get(username)

    if not query:
        raise ValueError
    else:
        user = User(username)
        login_user(user)
        user.authenticated = True
        return redirect(url_for('user', username=username))


@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('home'))


def home():
    curr_id = current_user.get_id()
    if curr_id != None:
        return redirect(url_for('user', username=curr_id))
    else:
        return render_template('home.html')


@login_required
def user(username):
    curr_id = current_user.get_id()
    if username == curr_id:
        return render_template('user.html', username=username)
    else:
        return redirect(url_for('home'))
