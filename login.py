import os
import tabledb

from flask import Flask
from flask import flash, redirect, render_template, request, session, abort



def user(username):
    return 'Hello <h1>' + username + '</h1>'


def login():
    print('*\n'*10)
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    print(username)
    print(password)

    user_db = tabledb.db_session()

    query = user_db.query(tabledb.UserBase).get(username)

    if not query:
        raise ValueError
    else:
        session['logged_in'] = True
        return user(username)


def logout():
    session['logged_in'] = False
    return home()


def home():
    return render_template('login.html')
