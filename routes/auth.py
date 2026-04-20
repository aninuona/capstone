from flask import Blueprint, jsonify, request, session
from models import db, User
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    # Checks credentials, only proceeds if the account has the admin role
    data     = request.get_json()
    email    = data.get("email", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password."}), 401

    if user.role != "admin":
        return jsonify({"error": "Your account does not have admin access."}), 403

    session["user_id"] = user.id
    session["role"]    = user.role

    return jsonify({"message": "Logged in.", "role": user.role}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Clears the session
    session.clear()
    return jsonify({"message": "Logged out."}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    # Returns the currently logged in user 
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in."}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    return jsonify({"id": user.id, "email": user.email, "role": user.role}), 200
