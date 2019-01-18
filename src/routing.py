from flask import Flask,Blueprint
import src

Routing = Blueprint('Routing', __name__)

@Routing.route("/test/")
def test():
    return "response"

# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
