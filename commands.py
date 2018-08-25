import  games
import users
import utilities as utilities

def Handler(command, db):
    
    if(command == "addUser"):
        print("Adding User")
        username = input("Username:\n")
        bgg = input("Board Game Geeks Account:\n")
        u = users.User(username, 1, 0.5)
        u.scrapePreferences(bgg, db)
        db.Users.insert(u.dict())
        print("added user")
    
    elif(command == "deleteUser"):
        print("deleting user")
        username = input("Username:\n")
        users.deleteUser(db, username)
        print("deleted user")

    elif(command == "playedGame"):
    	game = input("Enter a played game:\n")
    	users.updateStack(game, db, "bob")

#    elif(command == ")



