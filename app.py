# FACULTY - POLICY BUILDER
@app.route('/build-policy', methods=['POST'])
def build_policy():
    data = request.json
    # like: {"q1": "Minimal Intervention", "q2": "Detailed Logs"}
    
    philosophy = data.get('q1')
    
    # logic
    if philosophy == "Minimal Intervention":
        tier = "T0 - Prohibited"
        compliance = "N/A"
        generated_text = "The use of generative AI is strictly prohibited for all assignments."
    else:
        tier = "T3 - Bounded Use"
        compliance = "C3 - Logs Required"
        generated_text = "AI use is permitted for brainstorming. You must provide a log of all prompts."

    # SQL save the newly built policy to database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO policies (course_name, policy_text, tier_id, compliance_id) VALUES (%s, %s, %s, %s)",
        ("Custom Course", generated_text, tier[:2], compliance[:2])
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "status": "success",
        "tier": tier,
        "text": generated_text
    })
