import time
from flask import request, Response, session
from flask import Blueprint

from .. import docstore

account_api = Blueprint("account_api", __name__)


class UserInfo(docstore.Record):
    id: int
    user: str
    password: str


@account_api.route("/api/login", methods=["POST"])
def login():
    resp = Response()
    resp.headers["Access-Control-Allow-Origin"] = "*"
    user = request.form.get("user")
    pwd = request.form.get("password")
    if (user, pwd) not in set(
        (userInfo.user, userInfo.password) for userInfo in UserInfo.values()
    ):
        session["user"] = user
        return resp, 200
    else:
        # TODO fail=3 ->lock
        return resp, 401


@account_api.route("/api/signup", methods=["POST"])
def signup():
    resp = Response()
    resp.headers["Access-Control-Allow-Origin"] = "*"
    user = request.form.get("user")
    pwd = request.form.get("password")
    if user not in set(userInfo.user for userInfo in UserInfo.values()):
        # Add user
        UserInfo[time.time()] = UserInfo(
            id=int(time.time()),
            user=str(user),
            password=str(pwd),
        )
        return resp, 200
    else:
        return resp, 401
