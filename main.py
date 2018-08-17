import numpy as np
from requests import get
from xml.dom import minidom
import string




class User:
	def __init__(self, name, id, variance):
		self.name = name
		self.id = id
		self.variance = variance
		self.preferences = []

	def addPreference(self, preference):
		self.preferences.append(preference)

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

	def getGame(self):
		return self

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
		self.game = getStats(name)
		self.userRating = userRating

	def getPreference(self):
		return self

	def __repr__(self):
		return "Game: " + str(self.game) + "\nuserRating: " + str(self.userRating)

def addGame (name):
	#Scrapes BGG for game info

	game = Game(name, 7.2, 2.1)
	return game;

def createPreference (name, userRating):

	game = addGame(name)
	preference = Preference(game, userRating);
	return preference

def getStats (name):

	#Get id of board game
	url = 'https://www.boardgamegeek.com/xmlapi/search?search=' + name + '&exact=1'
	response = get(url)
	xml = minidom.parseString(response.text)
	boardgame = xml.getElementsByTagName('boardgame')
	id = boardgame[0].attributes['objectid'].value

	#Get Stats from id
	url = 'https://boardgamegeek.com/xmlapi/boardgame/' + str(id) + '?&stats=1'
	response = get(url)
	text = response.text

	#filter out non ascii characters for xml parse
	printable = set(string.printable)
	text = filter(lambda x: x in string.printable, text)

	xml = minidom.parseString(text)

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

if __name__== "__main__":

	# g1 = Game("Red7", 7.2, 2.1, 15)
	# g2 = Game("Catan", 8.2, 2.3, 75)
	# g3 = Game("Seven Wonders", 7.5, 2.32, 60)
	# g4 = Game("Pocket Ops", 8.2, 2.3, 10)
	# g5 = Game("Gravwell", 7.1, 1.7, 20)
	# g5 = Game("Monopoly", 1.0, 0.1, 700)


	u = User("Kyle", 1, 0.5)

	p = Preference("Monopoly", 1)


	u.addPreference(p.getPreference)

	print(u)

	# print(getStats("Catan"))


