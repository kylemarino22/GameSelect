import string
import pymongo
import time
import src.utilities as util
from math import e
from .main import db

PLAYERCOUNT_CONST = 1
STACK_CONST = 3
AVERAGE_CONST = 1

class GameSelector:


	def __init__(self, Users, minTime, maxTime):

		self.Users = Users
		self.maxTime = maxTime
		self.minTime = minTime

	def getAvailableGames(self):
		availableGames = []
		for User in self.Users:
			print(User)
			userGamesCursor = db.Users.find({'User': User}, {"gamesOwned.id":1})

			for obj in userGamesCursor:
				gamesObjList = obj['gamesOwned']

				for game in gamesObjList:

					gameID = game['id']

					if gameID not in availableGames:
						availableGames.append(gameID)


		self.availableGames = availableGames
		# print(availableGames)

	def genGameScore(self, gameID):
		obj = db.Games.find({'id':gameID})[0]

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
		stack_score = 0
		NA_counter = 0
		empty_stack_counter = 0
		for userName in self.Users:
			userRatingObj = db.Users.find_one({'User': userName,'gamesOwned.id': gameID},
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

			stack_index_Obj = db.Users.aggregate([
													{ '$match': { 'User': userName } },
													{ '$project': { 'matchedIndex': { '$indexOfArray': [ '$gameStack', gameID ] } } }
													] )
			stack_index = stack_index_Obj.next()['matchedIndex']

			if(stack_index == -1):
				stack_score += 1
			else:
				stack_score += self.calcStackScore(stack_index)





		try:
			averageRating = averageRating/(len(self.Users) - NA_counter)/10
		except ZeroDivisionError:
			print("All Scores are N/A!")
			averageRating = 0.5

		try:
			stack_score = stack_score/(len(self.Users))
		except ZeroDivisionError:
			print("All stacks are empty")
			stack_score = 1


		print(stack_score)
		score = averageRating * AVERAGE_CONST + playerCountScore * PLAYERCOUNT_CONST + stack_score * STACK_CONST


		# average = obj[]
		print("Average Rating: " + str(averageRating))
		print("Score: " + str(score))
		return score;


	def calcStackScore(self, index):

		n = len(self.availableGames) #Number of games
		H = 1.05 #Magic Number chosen that provides slope of logistic function
		K = -10/(n**H) #Changes the slope of function
		B = 3 #Changes where the inflection point is

		numerator = 1.1 #Scales function from -0.1 to 1
		denominator = 1 + e**(K * (index - n/B))

		return (numerator/denominator) - 0.1

	def genAllScores(self):
		gameScores = []
		self.getAvailableGames()

		maxScore = 0;
		pos = 0;
		for availableGame in self.availableGames:

			t = {'e':{}}
			t['e']['name'] = util.idToName(availableGame)
			t['e']['id'] = availableGame
			t['w'] = self.genGameScore(availableGame)
			if(t['w'] > maxScore):
				maxScore = t['w']
				pos = len(gameScores)

			if(t['w'] > 0):
				gameScores.append(t)


		#Sort and Validate Scores
		sortedScores = sorted(gameScores, key = lambda i: i['w'])
		print(sortedScores)
		print("=======================================\n")
		validScores = sortedScores[-int((len(sortedScores)/4)):]
		print(validScores)

		#valid scores should be mapped to a range from 0-1 before WeightedList
		weightList = [elem['w'] for elem in validScores]
		minWeight = min(weightList)
		maxWeight = max(weightList)

		for elem in validScores:
			elem['w'] = util.mapRange(elem['w'], minWeight, maxWeight, 1,2)

		#Weight the scores based on probability
		wl = util.WeightedList(validScores)

		print(wl.list)
		print("\n=====================================\n")
		print("Recommended Game:\n")
		print(wl.random())

		return gameScores[pos]
