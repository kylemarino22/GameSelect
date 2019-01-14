import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
import time
import utilities as util

PLAYERCOUNT_CONST = 0.5
QUEUE_CONST = 3
AVERAGE_CONST = 3

class GameSelector:


	def __init__(self, Users, minTime, maxTime, db):

		self.Users = Users
		self.maxTime = maxTime
		self.minTime = minTime
		self.db = db

	def getAvailableGames(self):
		availableGames = []
		for User in self.Users:
			print(User)
			userGamesCursor = self.db.Users.find({'User': User}, {"gamesOwned.id":1})

			for obj in userGamesCursor:
				gamesObjList = obj['gamesOwned']

				for game in gamesObjList:

					gameID = game['id']

					if gameID not in availableGames:
						availableGames.append(gameID)


		self.availableGames = availableGames
		# print(availableGames)

	def genGameScore(self, gameID):
		obj = self.db.Games.find({'id':gameID})[0]

		maxplaytime = obj["maxplaytime"]
		if(maxplaytime > self.maxTime):
			print("game too long")
			return -100

		try:
			playerCountScore = obj["playercountpoll"][str(len(self.Users))]
		except KeyError:
			print("player count too high")
			return -100

		if(playerCountScore < 0):
			print("playerCountScore too low")
			return -100

		averageRating = 0
		NA_counter = 0;
		for userName in self.Users:
			userRatingObj = self.db.Users.find_one({'User': userName,'gamesOwned.id': gameID},
														{'gamesOwned.$.userRating': 1});

			if(userRatingObj == None):
				print("User: " + userName + " does not exist");
				rating = 'N/A'
			else:
				rating = userRatingObj['gamesOwned'][0]['userRating']
			print(userName + ": " + str(rating))

			if(rating == 'N/A'):
				NA_counter += 1;
			else:
				averageRating += rating

		try:
			averageRating = averageRating/(len(self.Users) - NA_counter)/10
		except ZeroDivisionError:
			print("All Scores are N/A!")
			averageRating = 0.5

		score = averageRating * AVERAGE_CONST + playerCountScore * PLAYERCOUNT_CONST


		# average = obj[]
		print("Average Rating: " + str(averageRating))
		print("Score: " + str(score))
		return score;


	def genAllScores(self):
		gameScores = []
		self.getAvailableGames()

		maxScore = 0;
		pos = 0;
		for availableGame in self.availableGames:

			t = {}
			t['name'] = util.idToName(availableGame,self.db)
			t['id'] = availableGame
			t['score'] = self.genGameScore(availableGame)
			if(t['score'] > maxScore):
				maxScore = t['score']
				pos = len(gameScores)

			gameScores.append(t)

		print(gameScores)
		print("\n=====================================\n")
		print("Recommended Game:\n")
		print(gameScores[pos])
