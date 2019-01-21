<<<<<<< HEAD
<<<<<<< HEAD
import settings
from flask import Flask,Blueprint,request
=======
from flask import Flask,Blueprint
>>>>>>> refactor and flask beginning
=======
from flask import Flask,Blueprint,request
>>>>>>> saving progress
import src

Routing = Blueprint('Routing', __name__)

@Routing.route("/test/")
def test():
    return "response"

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> saving progress
@Routing.route("/addUser/", methods=['Post'])
def addUser():
    req_data = request.get_json()
    username = req_data['username']

    return "Response: " + str(username)
<<<<<<< HEAD
=======
>>>>>>> refactor and flask beginning
=======
>>>>>>> saving progress
# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
