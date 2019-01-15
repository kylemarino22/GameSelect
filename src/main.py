import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo

import users
import utilities
import commands
import gameselect



if __name__== "__main__":

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["GameSelect"]

	Users = mydb.Users

	while(1):
		inputCommand = input("Enter a Command:\n")

		if(inputCommand == "q"):
			break

		if(inputCommand == "test"):
			b = {'name': "Kyle",
				'age': 18,
				'Chad': "Yes"}
			c = {'name': "Shaheen",
				'age': 18,
				'Chad': "No"}
			d = {'name': "Jamsheed",
					'age': 18,
					'Chad': "No"}
			a = [{'e': b, 'w':4},
				{'e': c,'w':1},
				{'e':d, 'w': 2}]

			wl = utilities.WeightedList(a)
			for x in range(100):
				print(wl.random())
			# gs = gameselect.GameSelector(["Bob","a","b","c","d"], 10, 100, mydb)
			# game = gs.genAllScores()
			#
			# inputCommand = input("Will you play this game")
			#
		commands.Handler(inputCommand, mydb)
