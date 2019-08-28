#request group

from flask import Flask,request, jsonify, abort, g
from flask_httpauth import HTTPBasicAuth

import os
import logging
import sys
import src.users as users
import src.login
from .main import app, db

auth = HTTPBasicAuth()

@app.route('/api/createLobby', methods=['POST'])
@auth.login_required
def createLobby():
	f_usernames = request.json.get('f_usernames')

	for username in f_usernames:
		db.Users.update({'User': username},
						{'$set': {'gameRequest':g.user.username}},
						upsert = True)

	db.Users.update({'User': g.user.username},
					{'$set': {"lobby" : []}})
	return jsonify({"status": "ok"})


#join lobby
@app.route('/api/joinLobby', methods=['POST'])
@auth.login_required
def joinLobby():

	#user which has created the lobby
	f_username = request.json.get('f_username')

	#Game Request came from person that was confirmed

	if f_username == db.Users.find_one({'User':g.user.username})['gameRequest']:
		print("a", file = sys.stderr)
		db.Users.update({'User': f_username},
						{'$push': {'lobby':g.user.username}})
		return jsonify({"status": "ok"})

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

#creates a lobby under main user with friends
