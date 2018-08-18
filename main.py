import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo

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


	def addGame(self, name, rating):

		self.gamesOwned.append(Preference(name, rating));

	def __repr__(self):

		s = "User: " + self.name + "\nid: " + str(self.id) + "\nvariance: " + str(self.variance) + "\npreferences: "
		for p in self.preferences:
			s += str(p)
		return s

class Game:

	def __init__(self, name, average, bayesaverage, averageweight,
			minplaytime, maxplaytime, minplayers, maxplayers):

		self.name = name
		self.average = average
		self.bayesaverage = bayesaverage
		self.averageweight = averageweight
		self.minplaytime = minplaytime
		self.maxplaytime = maxplaytime
		self.minplayers = minplayers
		self.maxplayers = maxplayers


	def __repr__(self):

		return ("\nName: " + self.name +
			"\naverage: " + str(self.average) +
			"\nbayesaverage: " + str(self.bayesaverage) +
			"\naverageweight: " + str(self.averageweight) +
			"\nminplaytime: " + str(self.minplaytime) +
			"\nmaxplaytime: " + str(self.maxplaytime) +
			"\nminplayers: " + str(self.minplayers) +
			"\nmaxplayers: " + str(self.maxplayers))

class Preference:

	def __init__(self, name, userRating):
		self.name = name
		self.userRating = userRating

	def dict(self):
		return {'Game': self.name,
				'userRating': self.userRating}

	def __repr__(self):

		return "\nGame: " + str(self.game) + "\nuserRating: " + str(self.userRating)

def getStats (name):

	#Get id of board game
	url = 'https://www.boardgamegeek.com/xmlapi/search?search=' + name + '&exact=1'
	response = get(url)
	xml = parseString(response.text)
	boardgame = xml.getElementsByTagName('boardgame')
	id = boardgame[0].attributes['objectid'].value

	#Get Stats from id
	url = 'https://boardgamegeek.com/xmlapi/boardgame/' + str(id) + '?&stats=1'
	response = get(url)
	text = response.text

	# print (text)
	#filter out non ascii characters for xml parse
	printable = set(string.printable)
	text = "".join(list(filter(lambda x: x in string.printable, text)))

	# print(text)
	xml = parseString(text)

	average = xmlHandler(xml, 'average')
	bayesaverage = xmlHandler(xml, 'bayesaverage')
	averageweight = xmlHandler(xml, 'averageweight')
	minplaytime = xmlHandler(xml, 'minplaytime')
	maxplaytime = xmlHandler(xml, 'maxplaytime')
	minplayers = xmlHandler(xml, 'minplayers')
	maxplayers = xmlHandler(xml, 'maxplayers')

	return Game(name, float(average), float(bayesaverage), float(averageweight),
		int(minplaytime), int(maxplaytime), int(minplayers), int(maxplayers))

def xmlHandler(xml, tag):

	return xml.getElementsByTagName(tag)[0].firstChild.nodeValue


class GameSelector:

	def __init__(self, Users, Games, minTime, maxTime):

		self.Users = Users
		self.Games = Games
		self.minTime = minTime
		self.maxTime = maxTime

	def selectGame(self):
		return "Sheriff+of+Nottingham"


if __name__== "__main__":

	boardgameList = ["Monopoly", "Catan", "Pocket+Ops",
					 "7+Wonders", "Sheriff+of+Nottingham", "Splendor",
					 "Gravwell:+escape+from+the+9th+dimension", "New+Angeles", "Cosmic+Encounter",
					 "Codenames", "The Resistance"]


	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["GameSelect"]

	Users = mydb.Users

	u1 = User("Kyle", 1, 0.5)
	u1.addGame("Monopoly", 3)
	u1.addGame("Catan", 6)
	u1.addGame("Pandemic", 9)

	# print(dict(u1))

	Users.insert(u1.dict())

	# print(u2)



