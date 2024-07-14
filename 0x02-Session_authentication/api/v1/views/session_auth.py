#!/usr/bin/env python3
""" Module of Session Authentication """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """Handle user login using session authentication.

    This route allows users to log in by providing their email and password
    If the email or password is missing, an error message is returned
    If the email is not associated with any user, an error message is returned
    If the password is incorrect, an error message is returned.
    If the login is successful, a session is created and a user object
    JSON is returned

    Returns:
        A JSON response containing the user object.

    Raises:
        400: If email or password is missing.
        404: If no user is found for the provided email.
        401: If the password is incorrect.

    """
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_name = getenv("SESSION_NAME")
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(session_name, session_id)
    return response


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """Handle user logout using session authentication.

    This route allows users to log out by destroying their session
    If the session cookie is missing, an error message is returned
    If the session cookie is invalid, an error message is returned
    If the logout is successful, an empty JSON response is returned

    Returns:
        An empty JSON response.

    Raises:
        403: If the session cookie is missing or invalid.

    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
