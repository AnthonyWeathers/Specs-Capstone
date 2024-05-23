import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255) , nullable = False)
    password = db.Column(db.String(255) , nullable = False)

    owned_poke = db.relationship("OwnPoke", backref = "move", lazy = True)

class Move(db.Model):

    __tablename__ = "moves"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String , nullable = False)
    power = db.Column(db.Integer , nullable = True)
    accuracy = db.Column(db.Integer , nullable = True)
    pp = db.Column(db.Integer , nullable = False)

class Poke(db.Model):

    __tablename__ = "pokemon"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    poketype1 = db.Column(db.Integer, db.ForeignKey("types.id"), nullable = False)
    poketype2 = db.Column(db.Integer, db.ForeignKey("types.id"), nullable = True)

class PokeMove(db.Model):

    __tablename__ = "pokemon_moves"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), nullable = False)
    move_id = db.Column(db.Integer, db.ForeignKey("moves.id"), nullable = False)

class OwnPoke(db.Model):

    __tablename__ = "owned_pokes"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    sprite = db.Column(db.String(255), nullable = False)
    move_1_id = db.Column(db.Integer, db.ForeignKey("moves.id"), nullable = False)
    move_2_id = db.Column(db.Integer, db.ForeignKey("moves.id"), nullable = False)
    move_3_id = db.Column(db.Integer, db.ForeignKey("moves.id"), nullable = False)
    move_4_id = db.Column(db.Integer, db.ForeignKey("moves.id"), nullable = False)
    name = db.Column(db.String(255))
    poketype1 = db.Column(db.String(255))
    poketype2 = db.Column(db.String(255), nullable = True)

class PokeType(db.Model):
    __tablename__ = "types"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    poketype = db.Column(db.String(255), nullable = False)

class Region(db.Model):

    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    poketype = db.Column(db.String(255), nullable = False)

def connect_to_db(flask_app, echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)