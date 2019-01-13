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

		commands.Handler(inputCommand, mydb)
