from app import app
from app import mysql

from flask import render_template, request, redirect, jsonify, make_response

@app.route("/")
def index():
    return render_template("public/index.html")