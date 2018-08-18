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

	def addPreference(self, name, rating):

		self.preferences.append(Preference(name, rating));

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
		self.game = getStats(name)
		self.userRating = userRating

	def __repr__(self):

		return "Game: " + str(self.game) + "\nuserRating: " + str(self.userRating)

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


	u = User("Kyle", 1, 0.5)
	u.addPreference("Monopoly", 1.0)
	u.addPreference("Catan", 5.7)
	u.addPreference("Pocket+Ops", 7.3)

	print(u)



