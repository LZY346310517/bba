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

main = Blueprint('topic', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    return u


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    log(token, 'token11111')
    bs = Board.all()
    user = current_user()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user=user)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m)


@main.route("/delete")
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    log('删除 topic 用户是', u, id)
    # t.username = 'udade'
    # Topic.delete(id)
    # for reply in Reply.all(topic_id=id):
    #     Reply.delete(reply.id)
    # m = cls.query.filter_by(id=id).first()
    # db.session.delete(m)
    try:
        Topic.query.filter_by(id=id).delete()
        raise Exception('垃圾异常')
        Reply.query.filter_by(topic_id=id).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
    # 删除帖子和所有十条回复
    # 删除了帖子和三条回复
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))


@main.route("/profile")
def tode():
    user_name = current_user().username
    user_id = current_user().id
    print(user_id, 'user__id')
    mst = Reply.all(user_id=user_id)
    s = []
    for i in mst:
        s.append(Topic.one(id=i.topic_id))
    print(s, 's')
    user = current_user()
    ms = Topic.all()
    return render_template("profile.html", user=user, created=ms)