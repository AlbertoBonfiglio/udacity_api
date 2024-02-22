from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from backend.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, db_uri=SQLALCHEMY_DATABASE_URI):
    try:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
        db.app = app
        db.init_app(app)
        db.create_all()
    except Exception as err:
        # Log the error to the console
        print("Something went wrong", err)
        # rethrow it 
        raise err 
        

"""
Question
"""
class Question(db.Model): # type: ignore
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(Integer)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }

"""
Category
"""
class Category(db.Model): # type: ignore
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
