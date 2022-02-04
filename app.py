from flask import Flask,request,json
from werkzeug.exceptions import HTTPException
import calculate_order as co

app = Flask(__name__)

@app.route("/get_order_total")        # main route for order calculation
def get_order_total():
    response=co.calculate_total_order(request.json)
    return response

@app.errorhandler(HTTPException)      # Error handler for HTTP Errors
def handle_http_error(e):
    response = e.get_response()
    response.data=json.dumps({
        "Status":"Http Error",
        "Error code": e.code,
        "Error description": e.description
    })
    response.content_type="application/json"
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)