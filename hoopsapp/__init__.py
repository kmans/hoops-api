from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

import hoopsapp.hotfuzz

#flask app
app = Flask(__name__)

#setup configs
app.config.update(
	SECRET_KEY = 'N6$pDhsRKxmB12!xDjpCBJ2H15#cJdiZcj',
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kamil:A9!3YuynVNe@kamilodb.cork9gwkg1mu.us-east-1.rds.amazonaws.com/mydb',
	STATIC_ROOT = None,
	)

#init postgres
db = SQLAlchemy(app)

#must import after db initialized
import hoopsapp.models


#init restFul
api = Api(app)