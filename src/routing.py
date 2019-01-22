import src.globals as globals

from flask import Flask,Blueprint,request, jsonify, abort, g
from flask_httpauth import HTTPBasicAuth
import src.users as users
import os
import logging


Routing = Blueprint('Routing', __name__)
auth = HTTPBasicAuth()
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

@Routing.route('/api/token', methods=['POST'])
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({ 'token': token.decode('ascii') })



@Routing.route('/api/resource', methods=['POST'])
@auth.login_required
def get_resource():
	# print(g.user)
	globals.app.logger.info(g.user)
	return jsonify({ 'data': str(g.user)})

#=================================================#
@auth.verify_password
def verify_password(u, p):

	username_or_token = request.json.get('username')
	password = request.json.get('password')
	# first try to authenticate by token
	user = None
	user = users.User.verify_auth_token(username_or_token)
	if not user:
		# try to authenticate with username/password
		user = users.User(globals.mydb.Users.find_one({'User':username_or_token}))
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

#=================================================#
