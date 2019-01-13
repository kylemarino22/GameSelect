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
		users.deleteUser(db, username)
		print("deleted user")

	elif(command == "playedGame"):
		game = input("Enter a played game:\n")
		username = input("Username:\n")
		users.updateStack(game, db, username)

	elif (command == "addGametoUser"):
		input_name = input("Username:\n")
		selectedUser = db.Users.find_one({'User':input_name})
		if (selectedUser == None):
			print("User not found!")
			return
		else:
			input_game = input("Game:\n")
			gameToAdd = db.Games.find_one({'name':input_game})
			if (gameToAdd == None):
				print("does not exist")
				# TODO: path to scrape from bgg
				return
			else:
				input_rating = input('Rating:\n')
				userRating = 0
				if (input_rating != 'N/A'):
					userRating = int(input_rating)
				else:
					# puts N/A into db
					userRating = (input_rating)

				#Check if user has game
				for user_game in selectedUser['gamesOwned']:
					if gameToAdd['name'] == user_game['name']:
						user.updateRating(gameToAdd['name'], userRating, db, selectedUser['name'])
						return
				user.addGameOwned(Preference(gameToAdd['name'], userRating), db, selectedUser['name'])
