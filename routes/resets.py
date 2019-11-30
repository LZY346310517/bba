import os
import uuid

#import gevent
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    current_app
)
from flask_sqlalchemy import SQLAlchemy

from werkzeug.datastructures import FileStorage

from models.base_model import db
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.message import Messages
# from routes import current_user, cache
from routes import current_user

import json

from utils import log

main = Blueprint('resets', __name__)

dict_tokens = dict()
@main.route('/reset/send', methods=['POST'])
def send():
    username = request.form['username']
    user = User.one(username=username)
    token = str(uuid.uuid4())
    dict_tokens[token] = user.id
    Messages.send(
        title='忘记密码',
        content='http://localhost:3000/reset/view?token={}'.format(token),
        sender_id=user.id,
        receiver_id=user.id,
    )
    return redirect('/')


@main.route('/reset/view', methods=['GET'])
def view():
    token = request.args['token']
    log(token, 'token1111111')
    if token in dict_tokens:
        return render_template('resets_view.html', token=token)
    else:
        return redirect('/')


@main.route('/reset/update', methods=['POST'])
def update():
    passdword = request.form['password']
    log(request.form, 'form')
    log(passdword, 'passsword')
    token = request.form['token']
    if token in dict_tokens:
        user_id = dict_tokens[token]
        user = User.one(id=user_id)
        user.password = User.salted_password(passdword)
    return redirect('/')
