#request friends

@app.route('/api/requestGroup', methods=['POST'])
@auth.login_required
def get_resource():
    f_usernames = request.json.get('f_usernames')

    for username in f_usernames:
        db.Users.update({'User': username},
    					{'gameRequest':g.user.userName})
	return {"status": "ok"}


#friend verification




#creates a lobby under main user with friends
