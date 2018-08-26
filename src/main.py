import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo

import users
import utilities
import commands



class GameSelector:

	def __init__(self, Users, Games, minTime, maxTime):

		self.Users = Users
		self.Games = Games
		self.maxTime = maxTime

	def selectGame(self):
		return "Sheriff+of+Nottingham"


if __name__== "__main__":

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["GameSelect"]

	Users = mydb.Users

	while(1):
		inputCommand = input("Enter a Command:\n")

		if(inputCommand == "q"):
			break

		commands.Handler(inputCommand, mydb)
