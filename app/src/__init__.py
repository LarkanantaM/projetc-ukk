class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


# filepath: [auth.py](http://_vscodecontentref_/0)
from flask import Blueprint
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return 'Login page'

# filepath: c:\Users\GC\OneDrive\Documents\renew\python-web-app\src\app.py
from flask import Flask
from routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)# filepath: c:\Users\GC\OneDrive\Documents\renew\python-web-app\src\app.py
from flask import Flask
from routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)