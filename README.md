# Mini Pokemon Adventure app
Utilizes login and register to make an account for app. Allows user to search for pokemon and get a random pokemon and be able to flee or capture them with a chance of capture failing. If pokemon gets caught, then sprite turns into pokemon and user returns to main page. Can view PC which holds all pokemon that the user has captured, and can view the individual pokemon's details of moves, name, and sprite with ability to rename or release the pokemon.

## Technologies used:
* Javascript (front-end)
* Python (back-end)
* Flask
* Jinja2
* HTML, CSS
* postgresSQL

## Features:
* Login:
![Login page](/static/login-page.png)
    * Requires a username and password that has been registered into the database
    * Redirects to main page if login was successful
![Login Success page](/static/login-success.png)
    * Shows on main page
    
* Register:
![Register page](/static/register-page.png)
    * Requires a username, password, and re-entered password before clicking register button
    * Needs a unique username that has not already been used, otherwise gives alert of “user already exists”
    * Redirects to login page with success message
![Register Success](/static/register-success.png)
    * Displays on Login screen if registration was successful

* Main/fortune:
![Main page](/static/main-page.png)
    * Allows user search for random pokemon, go to PC, or logout

* Encounter:
![Random Pokemon Encounter](/static/initial-encounter.png)
    * Clicking "Search for wild pokemon" will redirect to an encounter page
    * Will display a randomly selected pokemon from all that has been added to the PokeAPI
    * The pokemon has a 10% chance of being a shiny variant
    * Displays message of "A wild {pokemon name} has appeared
    * Has capture or flee buttons
![Capture Success](/static/capture-success.png)
    * Pokemon sprite changes to a regular pokeball'
    * Text changes to indicate pokemon was captured
    * A return option is shown for user to go back to the main page
![Capture Fail](/static/capture-fail.png)
    * Page is kept the same except the message of "A wild {pokemon name} has appeared" is changed to it avoided the pokeball
    * User can attempt to capture the pokemon over and over until they catch it or decide to flee
    * Currently set capture rate to 50% but the condition can be modified

* PC:
![PC Page](/static/pc-page.png)
    * All pokemon the user has caught will be displayed in the order they were caught
![Pokemon Details](/static/pokemon-details.png)
    * Clicking on a pokemon will make a details link appear, clicking it will redirect to the pokemon details page

* Pokemon Details:
![Pokemon Details Page](/static/pokemon-details-page.png)
    * Displays details of the pokemon
        * 4 moves that the pokemon could learn in the games with their name, power, accuracy, and pp
        * The pokemon's name
        * Pokemon type
        * The pokemon's sprite
        * Has Rename, Back, and Release options
![Rename](/static/update-pokemon-name.png)
    * Clicking Rename will make a box appear to type a new name and a update name link
    * Inputting a new name and clicking update name will automatically update the pokemon's name
![Release](/static/pokemon-release.png)
    * Clicking release will delete the pokemon from the database and remove them from the PC list
    * Redirects user back to PC with the message displayed above

## Instructions on how to run a cloned repo
If a user wishes to try this app out on their own device, then there is some requirements needed to run this as I did, or equivalents:
* Programs used (may use equivalents if similar):
    * Visual Studio Code
    * Git
    * PostgreSQL (to setup the basebase name, password, and server port)

* Steps to install:
    * clone repo: git clone {insert github repo link of project}
    * create a virtual environment with python version 3.12.2 
    * at the root of the directory (where you'd see the public, server, and static folders, and other files), open terminal (I used a Git Bash terminal) and run pip install requirements.txt
    * download pgAdmin4 and make a user, make password without a "?", setup a database, and find the server port of it
        * create a config.sh file
            * create "export POSTGRES_URI=" and set = to postgres://postgres:{password}@localhost:{port}/{database name}
                * you would replace {password} with the password you use to access your database
                * replace {username} with the name of user account you created in Login/Group Roles with super user and can login
                * replace {port} with the port assigned to PostgreSQL 16, or the server under Servers that has your database
                * replace {database name} with the name you gave the database that will be used on local device
                * result would be export POSTGRES_URI=postgresql://{username}:{password}@localhost:{port}/{database name}

* To Setup and Run App:
    * in the terminal, enter "source config.sh"
    * then if you're setting up for the first time, or want to reset the database, then enter "python seed_database.py" (if using python 3)
    * After setup, enter "python server.py", the app will be live, and you'd open the url you see in the terminal, if it works then you'll see the login page, shown earlier
    * Now you can use the app
    * Note: If you close visual studio code and relaunch it, you'll need to redo "source config.sh" before "python server.py", because source config.sh establishes the connection to your database