from flask import Flask
from flask_mysql_connector import MySQL
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

CORS(app)

mysql = MySQL(app)

from app import query_views
from app import user_views
