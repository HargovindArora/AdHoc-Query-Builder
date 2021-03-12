from app import app
from app import mysql

from flask import render_template, request, redirect, jsonify, make_response

@app.route("/")
def index():

    SQL = "show tables;"
    # conn = mysql.connection
    # cur = conn.cursor()
    # cur.execute(SQL)
    # output = cur.fetchall()
    # print(output)

    df = mysql.execute_sql(SQL, to_pandas=True)
    tables = {}
    for col in df.columns:
        tables[col] = []
        for x in df[col]:
            tables[col].append(x)

    print(tables)

    return render_template("public/index.html", tables=tables)