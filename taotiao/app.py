import os
from flask import Flask
from resources.user import user_bp
from config import Config
from util.middlewares import jwt_authentication

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(user_bp)
app.config.from_object(Config)
app.before_request(jwt_authentication)

if __name__ == '__main__':
    app.run()

