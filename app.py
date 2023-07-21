from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r"/*")


@app.route("/checkout", methods=["GET"])
def checkout():
    return jsonify({"msg": "success"}), 200


if __name__ == "__main__":
    app.run(debug=True)
