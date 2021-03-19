from flask import Flask
from flask_mysql_connector import MySQL

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

mysql = MySQL(app)

from app import query_views
from app import user_views
