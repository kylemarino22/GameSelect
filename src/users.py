from xml.dom.minidom import parse, parseString
import string
import pymongo
import time
import hashlib
import os
import src.utilities as util
from flask import Flask
from src.main import app, db
from itsdangerous import (TimedJSONWebSignatureSerializer
						  as Serializer, BadSignature, SignatureExpired)

class User:

	def __init__(self, user=None):

		#Default constructor
		if type(user) is str:
			self.username = user
			self.gamesOwned = []
			self.stack = []

		#Converting mongo dict result to object
		elif type(user) is dict:
			self.username = user['User']
			self.gamesOwned = user['gamesOwned']
			self.stack = user['gameStack']
			self.password_hash = user['password_hash']
			self.password_salt = user['password_salt']

	def dict(self):

		gamesOwnedDict = []

		for game in self.gamesOwned:
			gamesOwnedDict.append(game.dict())

		return {'User': self.username,
				'password_hash' : self.password_hash,
				'password_salt' : self.password_salt,
				'gamesOwned': gamesOwnedDict,
				'gameStack' : self.stack}

	def scrapePreferences(self, username):
		url = 'https://boardgamegeek.com/xmlapi2/collection?username='+ username +'&stats=1&excludesubtype=boardgameexpansion&own=1'
		response = get(url)
		text = response.text

		xml = parseString(text)


		items = xml.getElementsByTagName("item")

		if items is None:
			print ("not ready yet")
			return

		for item in items:
			# get id of game
			game = item.getAttribute('objectid')
			#get rating of game
			rating = util.xmlAttrib(item, "rating", "value")

			if (rating != 'N/A'):
				self.gamesOwned.append(Preference(game, int(rating)))
			else:
				self.gamesOwned.append(Preference(game, rating))

			#check if the game is in global game list
			if(checkForGame(game)):
				gameName = util.xmlTag(item, "name")
				print(gameName + " doesn't exist")
				temp = util.getStats(item, gameName)
				gameurl = 'https://www.boardgamegeek.com/xmlapi2/thing?id='+str(temp['id'])+'&stats=1'
				# print(temp['id'])
				gameresponse = get(gameurl)
				gametext = gameresponse.text
				gamexml = parseString(gametext)
				counts = gamexml.getElementsByTagName('poll')[0].getElementsByTagName('results')
				countsdict = {}
				for c in counts:
					scores = {n.getAttribute('value'):n.getAttribute('numvotes') for n in c.getElementsByTagName('result')}
					countsdict[c.getAttribute('numplayers')] = calcPlayerRating(int(scores['Best']),
																				int(scores['Recommended']),
																				int(scores['Not Recommended']))
				temp['playercountpoll'] = countsdict
				addGame(temp)
				time.sleep(2)

	def __repr__(self):

		s = "User: " + self.username + "\nPassword: " + self.password_hash
		return s

	def generate_auth_token(self, expiration = 600):
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({ 'username': self.username })

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token

		user = User(db.Users.find_one({'User':data['username']}))

		return user

	def hash_password(self, password):
		self.password_salt = os.urandom(16)
		hash = hashlib.sha256()
		hash.update(bytes(password, "utf-8"))
		hash.update(self.password_salt)
		self.password_hash = hash.hexdigest()

	def verify_password(self, password):
		hash = hashlib.sha256()
		hash.update(bytes(password, "utf-8"))
		hash.update(self.password_salt)
		if(self.password_hash == hash.hexdigest()):
			return True
		return False





def checkForGame(gameID):
	Games = db.Games
	if Games.find_one({"id": int(gameID)}) is None:
		return 1

def addGame(gameDict):
	Games = db.Games
	Games.insert(gameDict)

def deleteUser(user):
	db.Users.delete_one({'User': user})

def deleteGame(game, user):
	db.Users.update({'User': user},
					{'$pull':{'gamesOwned':{'Game': game}}})

def updateStack(game, user):
	id= util.nameToID(game)

	db.Users.update({'User': user},
					{'$push': {'gameStack': {'$each': [id], '$position': 0}}})

	# Store the last 30 board games played
	db.Users.update({'User': user},
					{'$unset': {"gameStack.31": 1}})


def calcPlayerRating(Best, Recommended, notRec):

	if(Best + Recommended + notRec == 0):
		return 0
	if (Best+Recommended <= notRec):
		return -1
	num = 3*Best + 2 *Recommended -0*notRec
	den = (Best+Recommended+notRec)
	# *3 - 1 scales from -1-2
	return min((num / den) -1, 0.5)




# def updateRating(game, rating, user):
# 	db.Users.update({'User': user,'gamesOwned.Game': game},
# 					{'$set':{'gamesOwned.$.userRating': rating}})

def updateRating(name, rating, user):
	for index, gam in enumerate( db.Users.find_one({'User':user})['gamesOwned']):
		if db.Games.find_one({'id':gam['id'] } )['name'] == name:
			db.Users.update_one({'User':user},{'$set':{'gamesOwned.{}.userRating'.format(index):rating}})
			return
	pref = Preference(db.Games.find_one({'name':name})['id'],rating )
	db.Users.update_one({'User':user},{'$push':{'gamesOwned':pref.dict(db)}})
# def updateStack(db, user):
# 	db.Users.update({'User': user, 'gameStack'

def addToStack(stack, name):
	stack.insert(0, name)
	if(len(stack) > 30):
		stack.remove(30)

#    def addGame(name, rating, user):
#    self.gamesOwned.append(Preference(name, rating));


class Preference:

	def __init__(self, name, userRating):
		self.name = name
		self.userRating = userRating

	def dict(self):
		t = {'id': int(self.name), 'userRating': self.userRating}
		return t


	def __repr__(self):

		return "\nGame: " + str(self.name) + "\nuserRating: " + str(self.userRating)
