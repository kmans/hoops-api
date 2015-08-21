from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api, marshal_with, fields


#flask app
app = Flask(__name__)

#setup configs
app.config.update(
	SECRET_KEY = 'N6$pDhsRKxmB12!xDjpCBJ2H15#cJdiZcj',
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kamil:STteK8z2W3QvP7mWP0S8l6IHI1iSR@kamilodb.cork9gwkg1mu.us-east-1.rds.amazonaws.com/mydb',
	STATIC_ROOT = None,
	)

#init postgres
db = SQLAlchemy(app)

#init restFul
api = Api(app)

#must import after db initialized
from hoopsapp.models import Teams, Players
from hoopsapp.hotfuzz import extractOne
from hoopsapp.hoops import teamdict, playerdict, fixer, PlayersInTeam, TeamPIE, HotFuzzTeam, HotFuzzPlayer
from hoopsapp.api import NBAPlayers, NBATeams, HotFuzzPlayer, HotFuzzTeam, PlayerID, TeamID

