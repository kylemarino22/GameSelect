import src.globals

import src.users
import utilities as utilities

def Handler(command):

	if(command == "addUser"):
		print("Adding User")
		username = input("Username:\n")
		bgg = input("BoardGameGeek Account:\n")
		u = User(username, 1, 0.5)
		if bgg != "none":
			u.scrapePreferences(bgg)
		db.Users.insert(u.dict())
		print("added user")

	elif(command == "deleteUser"):
		print("deleting user")
		username = input("Username:\n")
		deleteUser(username)
		print("deleted user")

	elif(command == "playedGame"):
		game = input("Enter a played game:\n")
		username = input("Username:\n")
		updateStack(game, username)

	elif (command == "addGametoUser"):
		nm = input("Username:\n")
		user = db.Users.find_one({'User':nm})
		if user==None:
			return
		else:
			gm = input("Game:\n")
			game = db.Games.find_one({'name':gm})
			if game == None:
				print("does not exist")
				return
			else:
				rating = input('Rating:\n')
				if (rating != 'N/A'):
					rate = int(rating)

				else:
					rate = (rating)
				updateRating(gm,rate,nm)
