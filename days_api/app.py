"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def clear_history():
    """Clears the app history."""
    app_history.clear()


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=['POST'])
def between():
    """Between route function"""
    # ERROR HANDLE BELLOW
    data = request.json
    if list(data.keys()) != ['first', 'last']:
        return {
            "error": "Missing required data."
        }, 400

    first = data.get('first')
    last = data.get('last')
    # ERROR HANDLE ABOVE
    try:
        first = convert_to_datetime(first)
        last = convert_to_datetime(last)
        response_json = {
            "days": get_days_between(first, last)
        }

        add_to_history(request)
        return response_json, 200
    except (TypeError, ValueError):
        return {
            "error": "Unable to convert value to datetime."
        }, 400


@app.route("/weekday", methods=['POST'])
def weekday():
    """weekday route function"""
    data = request.json
    date_in = data.get('date')
    if list(data.keys()) != ['date']:
        return {
            "error": "Missing required data."
        }, 400
    try:
        date_in_datetime = convert_to_datetime(date_in)
        weekday_in = get_day_of_week_on(date_in_datetime)
        response_json = {
            "weekday": weekday_in
        }

        add_to_history(request)
        return response_json, 200
    except (TypeError, ValueError):
        return {
            "error": "Unable to convert value to datetime."
        }, 400


@app.route("/history", methods=['GET', 'DELETE'])
def history():
    """History route function"""
    if request.method == 'GET':
        args = request.args.to_dict()
        number = args.get('number')
        if number is None:
            number = '5'
        if not number.isdigit():
            return {
                "error": "Number must be an integer between 1 and 20."
            }, 400
        number = int(number)
        if number < 1 or number > 20:
            return {
                "error": "Number must be an integer between 1 and 20."
            }, 400
        # complete error handle above
        add_to_history(request)
        start_i = len(app_history) - number
        print(start_i)
        print(len(app_history))
        if start_i <= 0:
            start_i = 0
        response_json = app_history[start_i:]
        response_json = response_json[::-1]
        return response_json, 200

    if request.method == 'DELETE':
        clear_history()
        # add_to_history(request)
        return {
            "status": "History cleared"
        }, 200


@app.route("/current_age", methods=['GET'])
def current_age():
    """Current_age route function"""
    args = request.args.to_dict()
    date = args.get('date')
    if date is None:
        return {
            "error": "Date parameter is required."
        }, 400
    try:
        age = get_current_age(date)
    except TypeError:
        return {
            "error": "Value for data parameter is invalid."
        }, 400
    return {
        "current_age": age
    }, 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
