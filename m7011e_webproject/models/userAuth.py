#Authenticates the user and checks if the user is in the database
class userAuth:
    def __init__(self, db):
        self.db = db

    def authenticate(self, username, password):
        user = self.db.users.find_one({'username': username})
        
    