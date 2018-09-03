import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo

import users
import utilities
import commands



class GameSelector:

	def __init__(self, Users, minTime, maxTime, db):

		self.Users = Users
		self.maxTime = maxTime
		self.db = db


	def selectGame(self):
		availableGames = []
		for User in self.Users:
			print(User)
			userGamesCursor = self.db.Users.find({'User': User}, {"gamesOwned.Game":1})

			for obj in userGamesCursor:
				gamesObjList = obj["gamesOwned"]

				for game in gamesObjList:
					gameID = game["Game"]

					if gameID not in availableGames:
						availableGames.append(gameID)


		
		print(availableGames)




if __name__== "__main__":

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["GameSelect"]

	Users = mydb.Users

	while(1):
		inputCommand = input("Enter a Command:\n")

		if(inputCommand == "q"):
			break

		if(inputCommand == "test"):
			gs = GameSelector(["bob","a"], 10, 30, mydb)
			gs.selectGame()

		commands.Handler(inputCommand, mydb)
