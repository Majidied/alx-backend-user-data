#!/usr/bin/env python3
""" Main file """
from auth import Auth
from flask import Flask, Response, jsonify, request, abort, make_response


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def hello() -> str:
    """GET /
    Return:
      - a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    Register a user
    Return:
      - a message
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> "Response":
    """POST /sessions

    Returns:
        Response: JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email, "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
