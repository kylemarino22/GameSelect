import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
import time
import utilities as util

class User:

	def __init__(self, name, id, variance):

		self.name = name
		self.id = id
		self.variance = variance
		self.gamesOwned = []
		self.stack = []

	def dict(self, db):

		gamesOwnedDict = []

		for game in self.gamesOwned:
			gamesOwnedDict.append(game.dict(db))

		return {'User': self.name,
				'id': self.id,
				'variance': self.variance,
				'gamesOwned': gamesOwnedDict,
				'gameStack' : self.stack}

	def scrapePreferences(self, username, db):
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
			if(checkForGame(game, db)):
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
				addGame(temp, db)
				time.sleep(2)

	def __repr__(self):

		s = "User: " + self.name + "\nid: " + str(self.id) + "\nvariance: " + str(self.variance) + "\npreferences: "
		for p in self.preferences:
			s += str(p)
		return s

def checkForGame(gameID, db):
	Games = db.Games
	if Games.find_one({"id": int(gameID)}) is None:
		return 1

def addGame(gameDict, db):
	Games = db.Games
	Games.insert(gameDict)

def deleteUser(db, user):
	db.Users.delete_one({'User': user})

def deleteGame(game, db, user):
	db.Users.update({'User': user},
					{'$pull':{'gamesOwned':{'Game': game}}})

def updateStack(game, db, user):
	db.Users.update({'User':user},
					{'$push': {'gameStack': {'$each': [game], '$position': 0}}})

	# Store the last 30 board games played
	db.Users.update({'User':user},
					{'$unset': {"gameStack.31": 1}})


def calcPlayerRating(Best, Recommended, notRec):

	if(Best + Recommended + notRec == 0):
		return 0
	num = 3*Best + 2 *Recommended -0*notRec
	den = (Best+Recommended+notRec)
	# *3 - 1 scales from -1-2
	return (num / den) -1




def updateRating(game, rating, db, user):
	db.Users.update({'User': user,'gamesOwned.Game': game},
					{'$set':{'gamesOwned.$.userRating': rating}})

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

	def dict(self, db):
		t = {'id': int(self.name), 'userRating': self.userRating}
		return t

	def __repr__(self):

		return "\nGame: " + str(self.game) + "\nuserRating: " + str(self.userRating)
