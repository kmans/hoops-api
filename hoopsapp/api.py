from hoopsapp import api, Resource, Teams, Players, fields, jsonify, extractOne

#This function is used to normalize the data
#Also fixes issues with using map in Python 3
def fixer(data):
	for item in data:
		if item['_sa_instance_state']:
			del item['_sa_instance_state']
		elif item['_labels']:
			del item['_labels']
	return data

teams = fixer([t.__dict__ for t in Teams.query.all()])
#print(teams[0:3])

#gathering data as a list...
#test = list(Teams.query.with_entities(Teams.TEAM_NAME, Teams.TEAM_ID))
#print(test)

#This may not be needed...
'''
Team_resource_fields = {
	
	'TEAM_ID': fields.Integer,
	'TEAM_NAME': fields.String,
	'PIE': fields.Float,
}
'''


#get a JSON doc of all of the Teams in the NBA and all of their data
class NBATeams(Resource):
	def get(self):
		
		#return {'hello': 'world'}
		#return json.dumps([t.__dict__ for t in Teams.query.all()])
		teams = fixer([t.__dict__ for t in Teams.query.all()])
		#map(lambda k: k.pop('_sa_instance_state'), teams)
		return jsonify({'NBA Teams': teams})

class TeamID(Resource):
	def get(self, teamid):
		#print "TeamID is being called", teamid
		data = fixer([d.__dict__ for d in Teams.query.filter_by(TEAM_ID=teamid)])
		#map(lambda k: k.pop('_sa_instance_state'), data)
		return jsonify({'Team ID Result': data})


'''
Implemented my HotFuzz module here for fuzzy lookups of players or teams, will return exactly one
result as a best guess
'''
class HotFuzzTeam(Resource):
	def get(self, teamguess):
		#print "HotFuzzTeam is being called", teamguess
		teamlist = list(Teams.query.with_entities(Teams.TEAM_NAME, Teams.TEAM_ID))
		teamname = extractOne(teamguess, teamlist)[0][0]
		data = fixer([d.__dict__ for d in Teams.query.filter_by(TEAM_NAME=teamname)])
		return jsonify({'Result for Teamname lookup': data})

class HotFuzzPlayer(Resource):
	def get(self, playerguess):
		#print "HotFuzzPlayer is being called", playerguess
		playerlist = list(Players.query.with_entities(Players.PLAYER_NAME, Players.PLAYER_ID))
		playername = extractOne(playerguess, playerlist)[0][0]
		data = fixer([d.__dict__ for d in Players.query.filter_by(PLAYER_NAME=playername)])
		return jsonify({'Result for Playername lookup': data})



#get a JSON doc of all of the Players in the NBA and all of their data
class NBAPlayers(Resource):
	def get(self):
		players = fixer([p.__dict__ for p in Players.query.all()])
		return jsonify({'NBA Players': players})


class PlayerID(Resource):
	def get(self, playerid):
		#print "PlayerID is being called", playerid
		data = fixer([d.__dict__ for d in Players.query.filter_by(PLAYER_ID=playerid)])
		return jsonify({'Player ID Result': data})


#return back a all json data for teams, players
api.add_resource(NBATeams, '/api/teams')
api.add_resource(NBAPlayers, '/api/players')

#search by teamID, playerID
api.add_resource(TeamID, '/api/teams/id/<int:teamid>')
api.add_resource(PlayerID, '/api/players/id/<int:playerid>')

#fuzzy string matching via hotfuzz module
api.add_resource(HotFuzzTeam, '/api/teams/search/<teamguess>')
api.add_resource(HotFuzzPlayer, '/api/players/search/<playerguess>')