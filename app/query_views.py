from app import app
from app import mysql

from flask import render_template, request, redirect, jsonify, make_response


query = {}


@app.route("/get_tables")
def get_tables():

    SQL = "show tables;"

    df = mysql.execute_sql(SQL, to_pandas=True)
    tables = []

    for col in df.columns:
        for x in df[col]:
            tables.append(x)

    res = make_response(jsonify({"tables": tables}), 200)

    return res


@app.route("/table", methods=["POST"])
def table():

    req = request.get_json()

    try:
        table = req['table']
        tables = ", ".join(table)
        SQL = f"desc {tables};"

    except:
        return "No Table Found!", 400

    df = mysql.execute_sql(SQL, to_pandas=True)

    query["table"] = table

    cols = []

    for x in df['Field']:
        cols.append(x)

    res = make_response(jsonify({"columns": cols}), 200)

    return res


@app.route("/column", methods=["POST"])
def column():

    req = request.get_json()
    column = req['column']

    try:
        tables = ", ".join(query['table'])
        SQL = f"desc {tables};"
        df = mysql.execute_sql(SQL, to_pandas=True)

    except KeyError:
        return "No Table/Column Found!", 400

    cols = []

    for x in df['Field']:
        cols.append(x)

    if not column or column[0] == "all" or len(column) == len(cols):
        query["column"] = "*"
    else:
        if len(column) == 1:
            query["column"] = column[0]
        else:
            query["column"] = []
            for col in column:
                query["column"].append(col)

    res = make_response(jsonify({"message": "Columns Selected"}), 200)

    return res


@app.route("/conditions", methods=["POST"])
def where_clause():

    req = request.get_json()

    try:
        where = req["where"]
        conditions = where["conditions"]
        acceptance = where["acceptance"]

        where = ""

        if acceptance == "not all" or acceptance == "none":
            where += "NOT ("

        else:
            where += "("

        if acceptance == "all" or acceptance == "not all":
            for condition in conditions:
                where += condition
                where += " AND "
        elif acceptance == "any" or acceptance == "none":
            for condition in conditions:
                where += condition
                where += " OR "

        where = where.split()
        where.pop()
        where = " ".join(where)
        where += ")"

        query["where"] = where

        res = make_response(
            jsonify({"message": "Conditions Successfully selected"}), 200)

    except (TypeError, KeyError, NameError) as e:
        res = make_response(jsonify({"message": "Check payloads"}), 400)

    return res


@app.route("/generate_sql", methods=["GET"])
def generate_sql():

    table = query.get('table')
    column = query.get('column')
    where = query.get('where')
    group_by = query.get('group_by')
    aggregate = query.get('aggregate')
    having = query.get('having')

    try:
        columns = ", ".join(column)
        tables = ", ".join(table)

        SQL = f"SELECT {columns} FROM {tables}"

        if where:
            SQL += " WHERE "
            SQL += query["where"]

        SQL += ";"
        query["SQL"] = SQL

        res = make_response(jsonify({"SQL": SQL}), 200)

    except TypeError:
        res = make_response(
            jsonify({"message": "Improper Payloads"}), 400)

    return res


@app.route("/result", methods=["GET"])
def get_result():

    try:
        table = query.get('table')
        column = query.get('column')
        SQL = query.get('SQL')

        columns = ", ".join(column)
        tables = ", ".join(table)

        conn = mysql.connection
        cur = conn.cursor()
        cur.execute(SQL)
        output = cur.fetchall()

        res = make_response(
            jsonify({"tables": tables, "columns": columns, "result": output}), 200)

    except (TypeError, KeyError, NameError) as e:
        res = make_response(
            jsonify({"message": "Improper Payloads"}), 400)

    return res
