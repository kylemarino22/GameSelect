from flask import Flask,request, jsonify, abort, g
from flask_httpauth import HTTPBasicAuth

import os
import logging
import src.users as users
from .main import app, db

auth = HTTPBasicAuth()


@app.route('/api/users', methods = ['POST'])
def new_user():
	print (request.json)
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400) # missing arguments

	if db.Users.find_one({'User':username}) is not None:
		abort(400) # existing user


	user = users.User(username)
	user.hash_password(password)

	db.Users.insert(user.dict())

	return jsonify({ 'username': user.username }), 200

@app.route('/api/token', methods=['POST'])
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({ 'token': token.decode('ascii') })


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
		user = users.User(db.Users.find_one({'User':username_or_token}))
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

#=================================================#
