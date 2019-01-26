import pymongo
from flask import Flask
import src.config

app = Flask(__name__)
app.config.from_pyfile('config.py')
# app.register_blueprint(Routing)

db = pymongo.MongoClient("mongodb://localhost:27017/")["GameSelect"]

#api endpoints
import src.login
import src.lobby
