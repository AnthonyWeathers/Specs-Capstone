"""CRUD operations."""

from model import db, User, Move, PokeMove, OwnPoke, Poke, PokeType, connect_to_db
from sqlalchemy import or_

def create_user(username, password):
    """Create and return a new user."""

    user = User(username=username, password=password)

    return user

def get_users():
    """Return all users."""
    return User.query.all()

def get_user_by_id(id):
    """Return a user's profile."""
    return User.query.get(id)

def get_user_by_username(username):
    """Return a user's profile."""
    return User.query.filter(User.username == username).first()



def create_move(name, pp, power=None, accuracy=None):
    """Create and return a new move."""

    move = Move(name=name, power=power, accuracy=accuracy, pp=pp)

    return move

def get_moves():
    """Return all moves."""
    return Move.query.all()

def get_move_by_id(id):
    """Return a move's details."""
    return Move.query.get(id)

def get_move_by_name(name):
    """Return a move's details via given name."""
    return Move.query.filter_by(name=name).first()




def create_pokemon(name, poketype1, poketype2):
    """Create and return a new pokemon from database."""

    pokemon = Poke(name=name, poketype1=poketype1, poketype2=poketype2)

    return pokemon

def get_pokemon():
    """Return all pokemon."""
    return Poke.query.all()

def get_pokemon_by_id(id):
    """Return a pokemon details."""
    return Poke.query.get(id)

def get_pokemon_by_typeid(typeid):
    """ Return all pokemon that has the inputted type """
    return Poke.query.filter(
        or_(Poke.poketype1 == typeid, Poke.poketype2 == typeid)).all()



def create_poke_move(pokemon_id, move_id):
    """Create and return a new pokemon to move connection."""

    poke_move = PokeMove(pokemon_id=pokemon_id, move_id=move_id)

    return poke_move

def get_pokemon_moves():
    """Return all moves connected with pokemon."""
    return PokeMove.query.all()

def get_pokemon_move_by_poke_id(poke_id):
    """Return a move id connected to the pokemon."""
    return PokeMove.query.filter_by(pokemon_id=poke_id).all()



def create_own_poke(pokemon_id, user_id, sprite, move_1_id, move_2_id, move_3_id, move_4_id, name, poketype1, poketype2):
    """Create and return a new caught pokemon."""

    owned_pokemon = OwnPoke(pokemon_id=pokemon_id, user_id=user_id, sprite=sprite, move_1_id=move_1_id, 
                  move_2_id=move_2_id, move_3_id=move_3_id, move_4_id=move_4_id, name=name,
                  poketype1=poketype1, poketype2=poketype2)

    return owned_pokemon

def get_owned_pokemon():
    """Return all caught pokemon sorted."""
    return OwnPoke.query.all()

def get_owned_pokemon_by_id(id):
    """Return a caught pokemon's details."""
    return OwnPoke.query.get(id)

def get_owned_pokemon_by_user_id(user_id):
    """Return a caught pokemon's details."""
    return OwnPoke.query.filter_by(user_id=user_id).order_by(OwnPoke.id).all()

def get_owned_pokemon_by_typename(user_id, typename):
    """ Return all pokemon that has the inputted type and is owned by the logged user """
    return OwnPoke.query.filter(OwnPoke.user_id == user_id,
        or_(OwnPoke.poketype1 == typename, OwnPoke.poketype2 == typename)).all()

# PokeType crud functions
def create_poke_type(poketype):
    """Create and return a new pokemon to move connection."""

    poke_type = PokeType(poketype=poketype)

    return poke_type

def get_poke_type_by_type(type):
    """Return a type's name and id."""
    return PokeType.query.filter_by(poketype=type).first()

def get_poke_type_by_id(type_id):
    """Return a type's name and id."""
    return PokeType.query.filter_by(id=type_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)