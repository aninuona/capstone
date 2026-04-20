import random
from flask import Blueprint, jsonify, request
from models import db, PolicyFragment

game_bp = Blueprint("game", __name__)


@game_bp.route("/fragment", methods=["GET"])
def get_fragment():
    # a Returns one random policy fragment for the quiz
    count = PolicyFragment.query.count()
    if count == 0:
        return jsonify({"error": "No fragments in the database yet."}), 404

    fragment = PolicyFragment.query.offset(random.randint(0, count - 1)).first()
    return jsonify({
        "id":        fragment.id,
        "text":      fragment.text,
    }), 200


@game_bp.route("/check", methods=["POST"])
def check_answer():
    # b Receives the student's guesses and scores them against the correct answers
    data        = request.get_json()
    fragment_id = data.get("fragment_id")
    user_t      = data.get("user_t", "")
    user_c      = data.get("user_c", "")
    user_e      = data.get("user_e", "")

    fragment = PolicyFragment.query.get(fragment_id)
    if not fragment:
        return jsonify({"error": "Fragment not found."}), 404

    correct = 0
    if user_t == fragment.correct_t: correct += 1
    if user_c == fragment.correct_c: correct += 1
    if user_e == fragment.correct_e: correct += 1

    return jsonify({
        "score":     correct,
        "out_of":    3,
        "accuracy":  round((correct / 3) * 100),
        "correct_t": fragment.correct_t,
        "correct_c": fragment.correct_c,
        "correct_e": fragment.correct_e,
    }), 200


@game_bp.route("/fragment", methods=["POST"])
def add_fragment():
    # c Adds a new policy fragment to the database, admin use only
    data = request.get_json()
    text      = data.get("text", "").strip()
    correct_t = data.get("correct_t", "")
    correct_c = data.get("correct_c", "")
    correct_e = data.get("correct_e", "")

    if not all([text, correct_t, correct_c, correct_e]):
        return jsonify({"error": "All fields are required."}), 400

    fragment = PolicyFragment(
        text      = text,
        correct_t = correct_t,
        correct_c = correct_c,
        correct_e = correct_e,
    )
    db.session.add(fragment)
    db.session.commit()

    return jsonify({"message": "Fragment added.", "id": fragment.id}), 201
