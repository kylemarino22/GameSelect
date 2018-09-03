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


	def getAvailableGames(self):
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


		self.availableGames = availableGames
		print(availableGames)

	def genScore(self, gameID):
		gameCursor = self.db.Games.find({'id':gameID})
		for obj in gameCursor:

			maxplaytime = obj["maxplaytime"]
			if(maxplaytime > self.maxTime):
				print("game too long")
				return 0

			playerCountScore = obj["playercountpoll"][str(len(self.Users))]

			if(playerCountScore < 0):
				print("playerCountScore too low")
				return 0

			# average = obj[]
			print(obj)



if __name__== "__main__":

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["GameSelect"]

	Users = mydb.Users

	while(1):
		inputCommand = input("Enter a Command:\n")

		if(inputCommand == "q"):
			break

		if(inputCommand == "test"):
			gs = GameSelector(["bob","a"], 10, 29, mydb)
			gs.genScore(68448)

		commands.Handler(inputCommand, mydb)
