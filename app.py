from flask import Flask, request, Response, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r"/*")


@app.route("/api/checkout", methods=["GET"])
def checkout():
    return Response({"msg": "success"}), 200


@app.route("/api/login", methods=["POST"])
def login():
    resp = Response()
    resp.headers["Access-Control-Allow-Origin"] = "*"
    user = request.form.get("user")
    pwd = request.form.get("password")
    if user == "123@qq.com" and pwd == "123":
        session["user"] = user
        return resp, 200
    else:
        return resp, 401


if __name__ == "__main__":
    app.run(debug=True)
