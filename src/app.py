from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from os import environ
from dotenv import load_dotenv, dotenv_values
from resources.errors import errors

load_dotenv('.env')
app = Flask(__name__)
config = dotenv_values()
app.config.from_object(config)
api = Api(app, errors=errors)
app.config['JWT_SECRET_KEY']="secret-code"
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = [
    {
        "db": "users",
        "host": "db",
        "port": 27017,
        "alias": "default",
    }
]

initialize_db(app)
initialize_routes(api)

