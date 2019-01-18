<<<<<<< HEAD
import settings
from flask import Flask,Blueprint,request
=======
from flask import Flask,Blueprint
>>>>>>> refactor and flask beginning
import src

Routing = Blueprint('Routing', __name__)

@Routing.route("/test/")
def test():
    return "response"

<<<<<<< HEAD
@Routing.route("/addUser/", methods=['Post'])
def addUser():
    req_data = request.get_json()
    username = req_data['username']

    return "Response: " + str(username)
=======
>>>>>>> refactor and flask beginning
# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
