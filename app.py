from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/checkout", methods=["GET"])
def checkout():
    return jsonify({"msg": "success"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
