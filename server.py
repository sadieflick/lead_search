from flask import Flask, render_template, redirect, session, request, flash, url_for
# import the function connectToMySQL from the file mysqlconnection.py
from flask_bcrypt import Bcrypt
from mySQLconnection import connectToMySQL
import re
import math
from datetime import datetime


app = Flask(__name__)
bcrypt = Bcrypt(app) 

app.secret_key = "keepItSecretKeepItSafe"

# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('ajax_pagination')

# Global var for number of rows per page.
numRows = 10


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/user/info', methods=["POST"])
def info():

    #date stuff

    if len(request.form["date_from"]) > 0:
        from_python = datetime.strptime(request.form["date_from"], "%Y-%m-%d")
    else:
        from_python = datetime(1, 1, 1)
    if len(request.form["date_from"]) > 0:
        to_python = datetime.strptime(request.form["date_to"], "%Y-%m-%d")
    else:
        to_python = datetime.now()

    date_from = from_python.strftime("%Y-%m-%d %H:%M:%S")
    date_to = to_python.strftime("%Y-%m-%d %H:%M:%S")

    print(request.form)
    query = request.form["name"] + "%"

    offset = int(request.form["page"]) * numRows - numRows

    data = {
        "query": query,
        "date_from": date_from,
        "date_to": date_to,
        "offset": offset,
        "numRows": numRows
    }

    users = mysql.query_db("SELECT * from USERS WHERE first_name LIKE %(query)s AND created_at > %(date_from)s AND created_at < %(date_to)s LIMIT %(offset)s, %(numRows)s", data)
    count = mysql.query_db("SELECT count('first_name') from USERS WHERE first_name LIKE %(query)s AND created_at > %(date_from)s AND created_at < %(date_to)s", data)[0]["count('first_name')"]
    print(count)
    pages = math.ceil(count/numRows)

    return render_template('table.html', users=users, pages=pages)


if __name__ == "__main__":
    app.run(debug=True)
