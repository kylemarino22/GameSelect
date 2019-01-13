import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
import time
import utilities as util


class GameSelector:

	PLAYERCOUNT_CONST = 3
	QUEUE_CONST = 3
	AVERAGE_CONST = 3


	def __init__(self, Users, minTime, maxTime, db):

		self.Users = Users
		self.maxTime = maxTime
		self.minTime = minTime
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
		obj = self.db.Games.find({'id':gameID})[0]

		maxplaytime = obj["maxplaytime"]
		if(maxplaytime > self.maxTime):
			print("game too long")
			return 0

		playerCountScore = obj["playercountpoll"][str(len(self.Users))]

		if(playerCountScore < 0):
			print("playerCountScore too low")
			return 0


		for userName in self.Users:
			userRatingCursor = self.db.Users.find_one({'User': userName,'gamesOwned.Game': str(gameID)},
														{'gamesOwned.$.userRating': 1});

			# for obj in userRatingCursor:
			# 	userRatingObj = obj["gamesOwned"]
			#
			# 	for game in userRatingCursor:
			# 		rating = game["userRating"]
			# 		print(rating)


			print("here")
			print(userRatingCursor)



		# average = obj["average"]/10
		#
		# score = average * AVERAGE_CONST +
		# 		playerCountScore * PLAYERCOUNT_CONST +


		# average = obj[]
		print(obj)
