import src.globals
import src.config

import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
from flask import Flask

import src
from src.routing import Routing


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(Routing)


if __name__== "__main__":


	globals.mydb = pymongo.MongoClient("mongodb://localhost:27017/")["GameSelect"]

	app.run()


	Users = mydb.Users


	while(1):
		inputCommand = input("Enter a Command:\n")

		if(inputCommand == "q"):
			break

		if(inputCommand == "test"):


			# wl = utilities.WeightedList(a)
			# for x in range(100):
			# 	print(wl.random())
			gs = gameselect.GameSelector(["Bob","a","b","c","d"], 10, 100)
			game = gs.genAllScores()
			#
			# inputCommand = input("Will you play this game")
			#
		commands.Handler(inputCommand)
