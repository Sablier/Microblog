from flask import render_template, g
from flask_login import current_user, AnonymousUserMixin
from app import app


# 每次会话前都检查一下登录状态
@app.before_request
def before_request():
    g.user = current_user  # current_user 由 flask_login.utils提供


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    return render_template("index.html", user=user)
