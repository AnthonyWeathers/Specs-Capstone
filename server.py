from flask import Flask, render_template, redirect, flash, request, session, url_for, jsonify
import jinja2
from forms import LoginForm, RegisterForm
from model import connect_to_db, db
import crud

import random

import requests

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined # for debugging purposes



@app.route("/")
def homepage():
    # return render_template("base.html")
    return redirect('/login')

@app.route('/main')
def mainmenu():
    # gets user from the session's username
    username = session['username']
    return render_template("main.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user into site."""
    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check to see if a registered user exists with this username
        user = crud.get_user_by_username(username)
        if user and user.password == password:
            flash(f"Successfully logged in.")
            session["user_id"] = user.id
            session['username'] = user.username
            return redirect("/main")
        
        flash(f"Either username or password was incorrect, please try again.")
        return redirect('/login')

    # Form has not been submitted or data was not valid
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers new user into site."""
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data

        # Check to see if a registered user exists with this username

        if crud.get_user_by_username(username):
            flash(f"This username is already in use, please use another.")
            return redirect('/register')

        user = crud.create_user(username, password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account was successfully created and you can now login.")
        return redirect("/login")
    
    # Form has not been submitted or data was not valid
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    """Log user out."""

    del session["username"]
    del session["user_id"]
    flash("Logged out.")
    return redirect("/login")

@app.route("/pc")
def pc():
     user = session['user_id']
     pokemons = crud.get_owned_pokemon_by_user_id(user)
     return render_template("pc.html", pokemons=pokemons)

@app.route("/pokemon/random")
def random_poke():
    """ Grabs a random pokemon to display when the find random pokemon button is pressed """

    total_pokemon = len(crud.get_pokemon())

    RanNum = random.randrange(1, total_pokemon)
    pokemon = crud.get_pokemon_by_id(RanNum)

    req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{RanNum}").json()['forms'][0]['url']

    RanNum = random.randrange(1, 10)

    if RanNum > 1:
        pic = requests.get(req).json()['sprites']['front_default']
        shiny = 'no'
    else:
        pic = requests.get(req).json()['sprites']["front_shiny"]
        shiny = 'yes'

    """ pokemon represents the random pokemon, and pic will be a sprite of it """
    return render_template('battle.html', pokemon=pokemon, pic=pic, shiny=shiny)

# capture pokemon view
""" When caught, application will grab 4 moves the pokemon can know, base to hm/tm, likely from poke_moves,
    table where it keeps track of what pokemon has access to moves in moves table. Get id of pokemon from its name,
    use it to filter for moves linked to it in poke_moves, randomly grab 4, and assign to owned_poke

    Creates a owned_poke with pokemon's id and a user, and connect the 4 moves selected
    to it
"""
@app.route("/pokemon/capture/<poke_id>/<shiny>", methods=["POST"])
def capture(poke_id, shiny):

    RanNum = random.randrange(1, 10)

    if RanNum > 5:

        moves = crud.get_pokemon_move_by_poke_id(poke_id)

        pokemon = crud.get_pokemon_by_id(poke_id)
        next_url = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.id}").json()['forms'][0]['url']
        if shiny == "yes":
            sprite = requests.get(next_url).json()['sprites']['front_shiny']
        else:
            sprite = requests.get(next_url).json()['sprites']['front_default']
        user_id = session["user_id"]

        pokeball = requests.get(f"https://pokeapi.co/api/v2/item/4/").json()['sprites']['default']
        print(pokeball)

        random.shuffle(moves)

        num = 0
        poke_moves = []

        for move in moves:
            if num == 4:
                break
            poke_moves.append(move)
            num += 1
        # will have Move instances of the 4 random moves(id, name, power, accuracy, pp)
        owned_poke_moves = []
        for move in poke_moves:
            owned_poke_moves.append(crud.get_move_by_id(move.move_id))

        owned_poke = crud.create_own_poke(
                poke_id,
                user_id,
                sprite,
                owned_poke_moves[0].id,
                owned_poke_moves[1].id,
                owned_poke_moves[2].id,
                owned_poke_moves[3].id,
                pokemon.name
            )
        db.session.add(owned_poke)
        db.session.commit()

        # Return JSON response instead of redirecting
        return jsonify({
            "catch": True,
            "message": f"Caught {pokemon.name}",
            "pokeball_url": pokeball
        })

    else:
        pokemon = crud.get_pokemon_by_id(poke_id)
        return jsonify({
            "catch": False,
            "pokemon_name": pokemon.name
        })

@app.route("/pc/<poke_id>")
def details(poke_id):
    # need sprite from own_poke, used pokemon_id to query pokemon for its type and name
    # used move_id to query all info on each move
    owned_poke = crud.get_owned_pokemon_by_id(poke_id)
    pokemon = crud.get_pokemon_by_id(owned_poke.pokemon_id)
    move_1 = crud.get_move_by_id(owned_poke.move_1_id)
    move_2 = crud.get_move_by_id(owned_poke.move_2_id)
    move_3 = crud.get_move_by_id(owned_poke.move_3_id)
    move_4 = crud.get_move_by_id(owned_poke.move_4_id)

    return render_template("poke_details.html", owned_poke=owned_poke, pokemon=pokemon,
                           move_1=move_1, move_2=move_2, move_3=move_3, move_4=move_4)

@app.route("/api/delete/<poke_id>")
def delete_poke(poke_id):
    owned_poke = crud.get_owned_pokemon_by_id(poke_id)
    pokemon = crud.get_pokemon_by_id(owned_poke.pokemon_id)

    if owned_poke:
        db.session.delete(owned_poke)
        db.session.commit()
        flash(f"{owned_poke.name} was released back into the wild")
        return redirect('/pc')
    else:
        flash("Release error")
        return redirect('/pc')
    
@app.route("/api/update_name/<poke_id>", methods=["POST"])
def update_name(poke_id):

    new_name = request.json.get("new_name")

    owned_poke = crud.get_owned_pokemon_by_id(poke_id)

    if owned_poke:
        owned_poke.name = new_name
        
        db.session.commit()
        return jsonify ({
            "success": True,
            "message": "Renaming was a success",
            "new_name": owned_poke.name
        })
    else:
        return jsonify ({
            "success": False,
            "message": "Renaming error",
            "new_name": owned_poke.name
        })

        

if __name__ == "__main__":
#    app.env = "development"
    connect_to_db(app, echo=False)
    app.run(debug = True, port = 8000, host = "localhost")