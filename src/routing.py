import src.globals as globals

from flask import Flask,Blueprint,request, jsonify, abort
import src.users as users
import os
Routing = Blueprint('Routing', __name__)

# @Routing.route("/test/")
# def test():
#     return "response"
#
# @Routing.route("/addUser/", methods=['Post'])
# def addUser():
#     req_data = request.get_json()
#     username = req_data['username']
#
#     return "Response: " + str(username)


@Routing.route('/api/users', methods = ['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400) # missing arguments

	if globals.mydb.Users.find_one({'User':username}) is not None:
		abort(400) # existing user


	user = users.User(username)
	user.hash_password(password)

	globals.mydb.Users.insert(user.dict())

	return jsonify({ 'username': user.username }), 201

#=================================================#
# @auth.verify_password
# def verify_password(username, password):
#     user = User.query.filter_by(username = username).first()
#     if not user or not user.verify_password(password):
#         return False
#     g.user = user
#     return True

#=================================================#
