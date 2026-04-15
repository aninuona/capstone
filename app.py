import os
import sys
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
 
sys.path.insert(0, os.path.dirname(__file__))
 
from config import config
from models import db

# create & authorize Flask app
def create_app(env: str = None) -> Flask:
    env = env or os.environ.get("FLASK_ENV", "development")
 
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
 
    app = Flask(
        __name__,
        static_folder=frontend_dir,
        static_url_path="",
    )
 
    app.config.from_object(config[env])
 
    CORS(app, supports_credentials=True, origins=[
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:5173",
    ])
 
    db.init_app(app)

    from routes.auth    import auth_bp
    from routes.decoder import decoder_bp
    from routes.builder import builder_bp
    from routes.game    import game_bp
    from routes.admin   import admin_bp

    # blueprint files
    app.register_blueprint(auth_bp,    url_prefix="/api/auth")
    app.register_blueprint(decoder_bp, url_prefix="/api/decoder")
    app.register_blueprint(builder_bp, url_prefix="/api/builder")
    app.register_blueprint(game_bp,    url_prefix="/api/game")
    app.register_blueprint(admin_bp,   url_prefix="/api/admin")
 
    @app.route("/")
    def home():
        return send_from_directory(app.static_folder, "index.html")

    #static pages
    pages = {
        "/decoder":       "decoder.html",
        "/buildsyllabus": "buildsyllabus.html",
        "/traininggame":  "traininggame.html",
        "/admin":         "admin.html",
        "/login":         "login.html",
        "/dashboard":     "dashboard.html",
    }
 
    def make_page_view(filename):
        def view():
            return send_from_directory(app.static_folder, filename)
        return view
 
    for path, filename in pages.items():
        app.add_url_rule(
            path,
            endpoint=filename.replace(".html", ""),
            view_func=make_page_view(filename),
        )

    #error handling
    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "message": "Syllabus Decoder API is running."}), 200
 
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found."}), 404
 
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error."}), 500

    #auto create database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as ex:
            print(f"Could not auto-create tables: {ex}")
            print("Make sure MySQL is running and credentials in config.py are correct.")
 
    return app

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
