import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo

import users
import utilities



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

	u1 = users.User("Kyle", 1, 0.5)

	u1.scrapePreferences("Shaheenthebean", mydb)

	Users.insert(u1.dict())



