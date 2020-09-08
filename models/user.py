import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    # these column names must match with the self."names" variables in __init__ method
    # sqlalchemy will automatically add the "id" property to UserModel, even if it is not in the constructor
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # (username,) is used to make it a tuple
        row = result.fetchone()
        if row:
            user = cls(*row) # passing it as a set of argument = cls(row[0], row[1], row[2])
        else:
            user = None
        
        connection.close()
        return user
        '''

        # cls.query = SELECT * FROM users
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row) # passing it as a set of argument = cls(row[0], row[1], row[2])
        else:
            user = None
        
        connection.close()
        return user
        '''

        return cls.query.filter_by(id=_id).first()