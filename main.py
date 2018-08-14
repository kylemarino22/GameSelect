import numpy as np

class User:
	def __init__(self, name, id, variance):
		self.name = name
		self.id = id
		self.variance = variance
		self.preferences = []

	def addPreference(self, preference):
		self.preferences.append(preference)

	def __str__(self):
		s = "User: " + self.name + "\nid: " + str(self.id) + "\nvariance: " + str(self.variance) + "\npreferences: "
		for p in self.preferences:
			s += str(p)
		return s

class Game:
	def __init__(self, name, bggRating, bggComplexity):
		self.name = name
		self.bggRating = bggRating
		self.bggComplexity = bggComplexity

	def getGame(self):
		return self

	def __repr__(self):
		return "\nName: " + self.name + "\nbggRating: " + str(self.bggRating) + "\nggComplexity: " + str(self.bggComplexity)

class Preference:
	def __init__(self, game, userRating):
		self.game = game
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


if __name__== "__main__":
	u = User("Kyle", 1, 0.5)
	g = Game("Red7", 7.2, 2.1);
	p = Preference(g, 3)
	u.addPreference(p.getPreference)

	print(u)