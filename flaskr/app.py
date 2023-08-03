from flask import Flask, Response
from flask_cors import CORS
import os

import importlib

from . import docstore

from modules.account import account_api

# 从modules文件夹下加载所有Python模块
modules = [
    importlib.import_module("pykinezumiko.modules." + name, ".")
    for name in sorted(
        entry.name.removesuffix(".py")
        for entry in os.scandir("pykinezumiko/modules")
        if entry.name.endswith(".py")
        and entry.name.count(".") == 1
        or entry.is_dir()
        and "." not in entry.name
    )
]

# 为定义了记录类的模块分配文档数据库
databases = {
    name: docstore.Database(f"excel/{name}.xlsx", tables)
    for name, tables in (
        (
            module.__name__.rpartition(".")[2],
            tuple(
                v
                for v in module.__dict__.values()
                if isinstance(v, docstore.Table) and v.__module__ == module.__name__
            ),
        )
        for module in modules
    )
    if tables
}


app = Flask(__name__)
CORS(app, resources=r"/*")
app.secret_key = b"1145141919810"
app.register_blueprint(account_api)


@app.route("/api/checkout", methods=["GET"])
def checkout():
    return Response({"msg": "success"}), 200
