import os
import tabledb

from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for



def user(username):
    return render_template('user.html', username=username)


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
        session['logged_in'] = True
        # return user(username)
        return redirect(url_for('user', username=username))


def logout():
    session['logged_in'] = False
    return home()


def home():
    return render_template('login.html')
