from flask import jsonify

BASE_URL = "http://127.0.0.1:5000"  # Change this if deploying with a custom domain

def json_response(data=None, status=200, message=None):
    response = {"status": "success" if status < 400 else "error"}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return jsonify(response), status
