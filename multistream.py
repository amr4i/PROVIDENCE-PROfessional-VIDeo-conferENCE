import os
import tabledb

from camera import Camera

from flask import Flask
from flask import flash, redirect, render_template, request, url_for, Response
from functools import wraps
from flask_login import login_required, login_user, logout_user, current_user


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed():
    cam = Camera()
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
