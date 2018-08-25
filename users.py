import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
import time
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
				temp = games.getStats(item, game)
				gameurl = 'https://www.boardgamegeek.com/xmlapi2/thing?id='+str(temp['id'])+'&stats=1'
				gameresponse = get(gameurl)
				gametext = gameresponse.text
				gamexml = parseString(gametext)
				counts = gamexml.getElementsByTagName('poll')[0].getElementsByTagName('results')
				countsdict = {}
				for c in counts:
					countsdict[c.getAttribute('numplayers')] = {n.getAttribute('value'):n.getAttribute('numvotes') for n in c.getElementsByTagName('result')}
				temp['playercountpoll'] = countsdict
				addGame(temp, db)
				time.sleep(10)


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

def deleteUser(db, user):
    db.Users.delete_one({'User': user})

    def deleteGame(game, db, user):
        db.Users.update({'User': user},
                        {'$pull':{'gamesOwned':{'Game': game}}})

    def updateRating(game, rating, db, user):
        db.Users.update({'User': user,'gamesOwned.Game': game},
                        {'$set':{'gamesOwned.$.userRating': rating}})

#    def addGame(name, rating, user):
#        self.gamesOwned.append(Preference(name, rating));


class Preference:

	def __init__(self, name, userRating):
		self.name = name
		self.userRating = userRating

	def dict(self):
		return {'Game': self.name,
				'userRating': self.userRating}

	def __repr__(self):

		return "\nGame: " + str(self.game) + "\nuserRating: " + str(self.userRating)
