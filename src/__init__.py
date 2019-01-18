import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
from flask import Flask

import src
from src.routing import Routing


app = Flask(__name__)
app.register_blueprint(Routing)


if __name__== "__main__":
	app.run()

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["GameSelect"]

	Users = mydb.Users
	print("hello", file=sys.stdout)


	while(1):
		inputCommand = input("Enter a Command:\n")

		if(inputCommand == "q"):
			break

		if(inputCommand == "test"):
			gs = gameselect.GameSelector(["Bob","a","b","c","d"], 10, 100, mydb)
			gs.genAllScores()

		commands.Handler(inputCommand, mydb)
