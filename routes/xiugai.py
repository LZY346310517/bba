from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.base_model import db
from models.reply import Reply
from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('xiugai', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    return u


@main.route("/")
def index():
    user = current_user()
    return render_template("xiugai.html",  user=user)
