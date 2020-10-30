# Self.Card

A web app for users to build micro web pages. Built with Flask.

## Summary

  - [Getting Started](#getting-started)
  - [Built With](#built-with)
  - [Contributing](#contributing)
  - [Authors](#authors)

## Getting Started

If you'd like to run a local version instance of this app please follow these steps:
  1. Clone the repo into a folder of your choice.
  2. Initialize a virtual environment for your project. See: [https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/]
  3. Activate the virtual environment as shown in the link above.
  4. Open a terminal in the project directory
  5. Install the requirements with the command `pip install -r requirements.txt` (please ensure you are in the same directory as the requirements.txt file)
  6. Step one dir back from the SelfCard folder.
  7. Open a python REPL and type the following code (assumes the project lives in a folder called `project`):
    `from project import db, create_app
     db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration`
  8. In the terminal type `export FLASK_APP="SelfCard"`
  9. Finally, type flask run

### Prerequisites

You must have python 3.x installed.

## Built With

  - [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web framework
  - [SQLAlchemy](https://www.sqlalchemy.org/) - Database
  - [jQuery](https://jquery.com/) - Javascript library
  - [validation](https://pypi.org/project/validation/) - Python validation library

## Contributing

I don't think anyone would ever submit a PR but if you want to go ahead.


## Authors

  - **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)

   - **Tyler Goodman** - *Software Engineer* -
    [Tyler's Github](https://github.com/technicallyty),
    [My website](https://manthatsgood.dev)
    
   - **Waleed Ali** - *Software Engineer* -
    [Waleed's Github](https://github.com/WaleedAli9631)

