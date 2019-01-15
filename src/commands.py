from users import *
import utilities as utilities

def Handler(command, db):

	if(command == "addUser"):
		print("Adding User")
		username = input("Username:\n")
		bgg = input("BoardGameGeek Account:\n")
		u = User(username, 1, 0.5)
		if bgg != "none":
			u.scrapePreferences(bgg, db)
		db.Users.insert(u.dict(db))
		print("added user")

	elif(command == "deleteUser"):
		print("deleting user")
		username = input("Username:\n")
		deleteUser(db, username)
		print("deleted user")

	elif(command == "playedGame"):
		game = input("Enter a played game:\n")
		username = input("Username:\n")
		updateStack(game, db, username)

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
				updateRating(gm,rate,db,nm)
