from flask import Flask
from flask_mysql_connector import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.database.db import initialize_db
from app.database import models
from .user_routes import initialize_routes


import json

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

api = Api(app)
initialize_routes(api)

CORS(app)

jwt = JWTManager(app)

initialize_db(app)

mysql = MySQL(app)


bcrypt = Bcrypt(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return models.TokenBlocklist.is_jti_blacklisted(jti)


from app import query_views