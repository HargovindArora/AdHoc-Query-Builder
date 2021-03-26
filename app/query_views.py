from app import app
from app import mysql

from flask import render_template, request, redirect, jsonify, make_response

from decimal import Decimal

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
    table = req['table']

    query["table"] = table

    res = make_response(jsonify({"message": "Table Selected"}), 200)

    return res


@app.route("/get_columns", methods=["GET"])
def get_columns():

    try:
        tables = query["table"]
        SQL = f"desc {tables[0]};"
    except KeyError:
        return jsonify({"message": "No Table found!"}), 400

    df = mysql.execute_sql(SQL, to_pandas=True)

    columns = []

    for x in df['Field']:
        columns.append(x)

    res = make_response(jsonify({"columns": columns}), 200)

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
            query["column"] = column
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
        where_res = req["where"]
        conditions = where_res["conditions"]
        acceptance = where_res["acceptance"]

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


@app.route("/aggregate_function", methods=["POST"])
def agg_function():

    req = request.get_json()

    try:
        aggregate_res = req["aggregate"]
        columns = aggregate_res["columns"]
        functions = aggregate_res["functions"]

        aggregate = ""

        for function, column in zip(functions, columns):
            agg = function + "(" + column + ") "
            aggregate += agg

        aggregate = aggregate.split()
        aggregate = ", ".join(aggregate)

        query["aggregate"] = aggregate

        res = make_response(
            jsonify({"message": "Aggregate functions selected"}), 200)

    except (TypeError, KeyError, NameError) as e:
        res = make_response(jsonify({"message": "Check payloads"}), 400)

    return res


# @app.route("/groupby", methods=["POST"])
# def groupby_clause():

#     req = request.get_json()


@app.route("/generate_sql", methods=["GET"])
def generate_sql():

    table = query.get('table')
    column = query.get('column')
    where = query.get('where')
    group_by = query.get('group_by')
    aggregate = query.get('aggregate')
    having = query.get('having')

    try:

        tables = ", ".join(table)

        SQL = "SELECT"

        if aggregate:
            substring = f" {aggregate}"
            SQL += substring
        else:
            columns = ", ".join(column)
            SQL += f" {columns}"

        SQL +=  f" FROM {tables}"

        if where:
            SQL += " WHERE "
            SQL += where

        SQL += ";"

        query["SQL"] = SQL

        res = make_response(jsonify({"SQL": SQL}), 200)

    except TypeError:
        res = make_response(
            jsonify({"message": "Couldn't find sufficient values to construct query!"}), 400)

    return res


@app.route("/result", methods=["GET"])
def get_result():

    try:
        table = query.get('table')
        SQL = query.get('SQL')

        if query.get('aggregate'):
            columns = query.get('aggregate')
        else:
            columns = ", ".join(query.get('column'))

        tables = ", ".join(table)

        conn = mysql.connection
        cur = conn.cursor()
        cur.execute(SQL)
        output = cur.fetchall()

        result = []

        for row in output:
            record = []
            for val in row:
                if isinstance(val, Decimal):
                    record.append(str(val))
                else:
                    record.append(val)
            result.append(record)

        res = make_response(
            jsonify({"tables": tables, "columns": columns, "result": result}), 200)

    except (KeyError, NameError, TypeError  ) as e:
        res = make_response(
            jsonify({"message": "Couldn't execute SQL!"}), 400)

    return res


@app.route("/clear", methods=["GET"])
def clear_selections():

    query.clear()

    print(query)

    return jsonify({"message": "Selections removed"}), 200