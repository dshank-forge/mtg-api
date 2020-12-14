import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "magic_the_gathering"
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Deck(db.Model):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    format = Column(String)
    colors = Column(String)
    creator = Column(String)

    def __init__(self, title, format, colors, creator):
        self.title = title
        self.format = format
        self.colors = colors
        self.creator = creator

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Card(db.Model):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    colors = Column(String)
    cmc = Column(Integer)

    def __init__(self, name, type, colors, cmc):
        self.name = name
        self.type = type
        self.colors = colors
        self.cmc = cmc

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
