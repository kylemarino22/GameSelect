import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo

import games
import utilities as util

class User:

	def __init__(self, name, id, variance):

		self.name = name
		self.id = id
		self.variance = variance
		self.gamesOwned = []

	def dict(self):

		gamesOwnedDict = []

		for game in self.gamesOwned:
			gamesOwnedDict.append(game.dict())

		return {'User': self.name,
				'id': self.id,
				'variance': self.variance,
				'gamesOwned': gamesOwnedDict}

 #    def deleteUser(self):

 #    def deleteGame(self, name):

 #    def updateRating(self, name, rating):

	def addGame(self, name, rating):
		self.gamesOwned.append(Preference(name, rating));

	def scrapePreferences(self, username, db):
		url = 'https://boardgamegeek.com/xmlapi2/collection?username='+ username +'&stats=1&excludesubtype=boardgameexpansion'
		response = get(url)
		text = response.text

		xml = parseString(text)

		
		items = xml.getElementsByTagName("item")

		if items is None:
			print ("not ready yet")
			return

		for item in items:
			game = util.xmlTag(item, "name")
			rating = util.xmlAttrib(item, "rating", "value")

			if (rating != 'N/A'):
				self.gamesOwned.append(Preference(game, int(rating)))
			else:
				self.gamesOwned.append(Preference(game, rating))
			if(checkForGame(game, db)):
				print(game + " doesn't exist")
				# print(item.toprettyxml())
				addGame(games.getStats(item, game), db)


	def __repr__(self):

		s = "User: " + self.name + "\nid: " + str(self.id) + "\nvariance: " + str(self.variance) + "\npreferences: "
		for p in self.preferences:
			s += str(p)
		return s

def checkForGame(name, db):
	Games = db.Games
	if Games.find_one({"name": name}) is None:
		return 1

def addGame(gameDict, db):
	Games = db.Games
	Games.insert(gameDict)


class Preference:

	def __init__(self, name, userRating):
		self.name = name
		self.userRating = userRating

	def dict(self):
		return {'Game': self.name,
				'userRating': self.userRating}

	def __repr__(self):

		return "\nGame: " + str(self.game) + "\nuserRating: " + str(self.userRating)



