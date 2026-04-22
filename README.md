# capstone

pip install flask flask-cors flask-sqlalchemy werkzeug

python -c "
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    u = User(email='you@email.com', password_hash=generate_password_hash('yourpassword'), role='admin')
    db.session.add(u)
    db.session.commit()
    print('Admin created')
"

python app.py

