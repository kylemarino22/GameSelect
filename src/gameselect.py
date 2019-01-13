import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
import time
import utilities as util


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
		gameCursor = self.db.Games.find({'id':gameID})[0]
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
