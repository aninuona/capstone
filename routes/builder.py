from flask import Blueprint, jsonify, request, session
from models import db, Policy, BuilderQuestion

builder_bp = Blueprint("builder", __name__)


@builder_bp.route("/questions", methods=["GET"])
def get_questions():
    # a Returns all builder questions as JSON for the frontend form
    questions = BuilderQuestion.query.all()
    result = [
        {
            "id":       q.id,
            "question": q.question,
            "option_a": q.option_a,
            "value_a":  q.value_a,
            "option_b": q.option_b,
            "value_b":  q.value_b,
        }
        for q in questions
    ]
    return jsonify(result), 200


@builder_bp.route("/policies", methods=["GET"])
def get_policies():
    # b Returns all saved policies, most recent first
    policies = Policy.query.order_by(Policy.created_at.desc()).all()
    result = [
        {
            "id":            p.id,
            "course_name":   p.course_name,
            "policy_text":   p.policy_text,
            "tier_id":       p.tier_id,
            "compliance_id": p.compliance_id,
            "created_at":    str(p.created_at),
        }
        for p in policies
    ]
    return jsonify(result), 200


@builder_bp.route("/policies/<int:policy_id>", methods=["DELETE"])
def delete_policy(policy_id):
    # c Deletes a single policy by its ID, admin or faculty only
    policy = Policy.query.get(policy_id)
    if not policy:
        return jsonify({"error": "Policy not found."}), 404

    db.session.delete(policy)
    db.session.commit()
    return jsonify({"message": "Policy deleted."}), 200
