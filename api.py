from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api, marshal_with, fields
#from flask.ext.sqlalchemy import SQLAlchemy
from hoopsapp import app, db, api
from hoopsapp.models import Teams, Players

teams = [t.__dict__ for t in Teams.query.all()]
map(lambda k: k.pop('_sa_instance_state'), teams)
#print teams[0]


#print [t.__dict__ for t in Teams.query.all()][0]
#print [t.__dict__ for t in Teams.query.all()][1]

#players = Players.query.all()


#setup endpoints

Team_resource_fields = {
	
	'TEAM_ID': fields.Integer,
	'TEAM_NAME': fields.String,
	'PIE': fields.Float,

}


#get a JSON doc of all of the Teams in the NBA and all of their data
class NBATeams(Resource):
	def get(self):
		
		#return {'hello': 'world'}
		#return json.dumps([t.__dict__ for t in Teams.query.all()])
		teams = [t.__dict__ for t in Teams.query.all()]
		map(lambda k: k.pop('_sa_instance_state'), teams)
		return jsonify({'NBA Teams': teams})

class TeamID(Resource):
	def get(self, teamid):
		print "TeamID is being called", teamid
		data = [d.__dict__ for d in Teams.query.filter_by(TEAM_ID=teamid)]
		map(lambda k: k.pop('_sa_instance_state'), data)
		return jsonify({'Team ID Result': data})


#get a JSON doc of all of the Players in the NBA and all of their data
class NBAPlayers(Resource):
	def get(self):
		players = [p.__dict__ for p in Players.query.all()]
		map(lambda k: k.pop('_sa_instance_state'), players)
		return jsonify({'NBA Players': players})


class PlayerID(Resource):
	def get(self, playerid):
		print "PlayerID is being called", playerid
		data = [d.__dict__ for d in Players.query.filter_by(PLAYER_ID=playerid)]
		map(lambda k: k.pop('_sa_instance_state'), data)
		return jsonify({'Player ID Result': data})


api.add_resource(NBATeams, '/api/teams')
api.add_resource(TeamID, '/api/teams/id/<int:teamid>')

api.add_resource(NBAPlayers, '/api/players')
api.add_resource(PlayerID, '/api/players/id/<int:playerid>')



#execute
if __name__ == '__main__':
	app.run(debug=True)

