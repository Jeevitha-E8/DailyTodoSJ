
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = 'todotable'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    
    def __init__(self,name):
        self.name=name