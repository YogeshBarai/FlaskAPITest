from http import HTTPStatus
from flask import Flask, abort, jsonify, redirect, request, url_for
import pymysql

app = Flask(__name__)

# MySQL Configuration
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_password = 'yogesh'
mysql_db = 'world'
# Create MySQL Connection
connection = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    db=mysql_db,
    cursorclass=pymysql.cursors.DictCursor
)


def get_response_msg(data, status_code):
    message = {
        'status': status_code,
        'data': data if data else 'No records found'
    }
    response_msg = jsonify(message)
    response_msg.status_code = status_code
    return response_msg


## /api/v1/getcity?country=IND
@app.route("/getcity", methods=['GET'])
def getcity():
    try:
        countrycode = request.args.get('country', default='IND', type=str)
        query = f"SELECT * FROM city WHERE COUNTRYCODE='{countrycode.upper()}'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            city = cursor.fetchall()
            response = get_response_msg(city, HTTPStatus.OK)
            return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))

## /api/v1/health
@app.route("/health", methods=['GET'])
def health():
    try:
        db_status = "Connected to DB" if connection.open else "Not connected to DB"
        response = get_response_msg("I am fine! " + db_status, HTTPStatus.OK)       
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))

## /
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('health'))

## =================================================[ Routes - End ]

## ================================[ Error Handler Defined - Start ]
## HTTP 404 error handler
@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):    
    return get_response_msg(data=str(e), status_code=HTTPStatus.NOT_FOUND)


## HTTP 400 error handler
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(e):
    return get_response_msg(str(e), HTTPStatus.BAD_REQUEST)


## HTTP 500 error handler
@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return get_response_msg(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
## ==================================[ Error Handler Defined - End ]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')