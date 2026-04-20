from flask import Blueprint, jsonify, request
from models import db, Policy

decoder_bp = Blueprint("decoder", __name__)


def classify_policy(text: str) -> dict:
    # a Core classification logic, reads the syllabus text and returns tier codes
    # TODO replace these keyword checks with a proper ML model or Claude API call
    text_lower = text.lower()

    # b T-Tier: how much AI use is allowed
    if any(word in text_lower for word in ["prohibited", "not permitted", "strictly forbidden", "no ai"]):
        t_tier = "T0"
    elif any(word in text_lower for word in ["some exceptions", "limited cases"]):
        t_tier = "T1"
    elif any(word in text_lower for word in ["ask permission", "prior approval", "instructor approval"]):
        t_tier = "T2"
    elif any(word in text_lower for word in ["bounded", "brainstorm", "outline only", "limited use"]):
        t_tier = "T3"
    elif any(word in text_lower for word in ["with documentation", "disclose", "citation required"]):
        t_tier = "T4"
    elif any(word in text_lower for word in ["encouraged", "open use", "freely"]):
        t_tier = "T5"
    else:
        t_tier = "T2"

    # c C-Level: what disclosure/compliance is required
    if any(word in text_lower for word in ["log", "step-by-step", "full transcript"]):
        c_level = "C3"
    elif any(word in text_lower for word in ["describe how", "explain your use"]):
        c_level = "C2"
    elif any(word in text_lower for word in ["note if", "mention if", "indicate if"]):
        c_level = "C1"
    else:
        c_level = "C0"

    # d E-Level: what the penalty is for violations
    if any(word in text_lower for word in ["expulsion", "automatic failure", "academic dismissal"]):
        e_level = "E3"
    elif any(word in text_lower for word in ["will result in", "penalty", "grade reduction", "zero"]):
        e_level = "E2"
    elif any(word in text_lower for word in ["may result", "could affect"]):
        e_level = "E1"
    else:
        e_level = "E0"

    return {"t_tier": t_tier, "c_level": c_level, "e_level": e_level}


@decoder_bp.route("/classify", methods=["POST"])
def classify():
    # e API endpoint that accepts syllabus text and returns classification JSON
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No syllabus text provided."}), 400

    result = classify_policy(text)
    return jsonify(result), 200
