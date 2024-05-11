"""
    Script to seed database.
    You'll have to enter the password to your server twice to have your database perform the drop and create db
    After doing that and no errors pop up, you're good to run 
"""

import os
import requests

import crud
import model
import server

os.system("dropdb specs-capstone")

os.system('createdb specs-capstone')

model.connect_to_db(server.app)

def seed_moves():
    # Fetch data from PokeAPI for moves
    response = requests.get('https://pokeapi.co/api/v2/move/?limit=919')
    data = response.json()

    # Iterate over each move and populate the database
    for move in data['results']:
        move_data = requests.get(move['url']).json()
        move_instance = crud.create_move(
            name=move_data['name'],
            power=move_data['power'],
            accuracy=move_data['accuracy'],
            pp=move_data['pp']
        )
        model.db.session.add(move_instance)
    
    model.db.session.commit()

def seed_pokemon():
    response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1025') # grabs all pokemon
    data = response.json()

    # Iterate over each Pokemon and populate the database
    for pokemon in data['results']:
        pokemon_data = requests.get(pokemon['url']).json()
        pokemon_instance = crud.create_pokemon(
            name=pokemon_data['name'],
            poketype=pokemon_data['types'][0]['type']['name']
        )
        model.db.session.add(pokemon_instance)
    
    model.db.session.commit()

def seed_pokemon_moves():

    pokemon = crud.get_pokemon() # all pokemon in db

    # iterate over all pokemon and assign connections with pokemon to all moves that the api listed that pokemon has
    for poke in pokemon:
        moves = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke.id}').json()['moves']
        for move in moves:
            poke_move = crud.get_move_by_name(move['move']['name'])
            if poke_move:
                pokemon_move_instance = crud.create_poke_move(
                pokemon_id=poke.id,
                move_id=poke_move.id
                )
                model.db.session.add(pokemon_move_instance)
    
    model.db.session.commit()

# Call the seeding functions

with server.app.app_context():
    model.db.create_all()

    seed_moves()
    seed_pokemon()
    seed_pokemon_moves()