from app import app
from app import mysql

from flask import render_template, request, redirect, jsonify, make_response

query = {}

@app.route("/get_tables")
def get_tables():

    SQL = "show tables;"
    # conn = mysql.connection
    # cur = conn.cursor()
    # cur.execute(SQL)
    # output = cur.fetchall()
    # print(output)

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

    SQL = f"desc {table};"
    df = mysql.execute_sql(SQL, to_pandas=True)

    query["table"] = table
    print(query['table'])


    cols = []

    for x in df['Field']:
        cols.append(x)

    res = make_response(jsonify({"columns": cols}), 200)

    return res

# print(query)


@app.route("/column", methods=["POST"])
def column():

    req = request.get_json()
    column = req['column']

    try:
        SQL = f"desc {query['table']};"
        df = mysql.execute_sql(SQL, to_pandas=True)
    except KeyError:
        return "No Table Found!", 200

    cols = []

    for x in df['Field']:
        cols.append(x)

    if not column or column[0]=="all" or len(column)==len(cols):
        query["column"] = "*"
    else:
        if len(column) == 1:
            query["column"] = column[0]
        else:
            query["column"] = []
            for col in column:
                query["column"].append(col)

    print(query)

    
    
    return 'Done'