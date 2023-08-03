from flask import Flask, request, Response, session
from flask_cors import CORS
import os
import time
import importlib

from . import docstore
import hashlib

app = Flask(__name__)
CORS(app, resources=r"/*")
app.secret_key = b"1145141919810"


@app.route("/api/checkout", methods=["GET"])
def checkout():
    return Response({"msg": "success"}), 200


class UserInfo(docstore.Record):
    id: int
    user: str
    password: str


@app.route("/api/login", methods=["POST"])
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


@app.route("/api/signup", methods=["POST"])
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


module = importlib.import_module("flaskr.app")

docstore.Database(
    filename="database/user_info.xlsx",
    tables=tuple(
        v
        for v in module.__dict__.values()
        if isinstance(v, docstore.Table) and v.__module__ == module.__name__
    ),
)
