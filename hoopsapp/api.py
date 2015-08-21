from hoopsapp import api, Resource, Teams, Players, fields, jsonify, \
extractOne, teamdict, playerdict, fixer, PlayersInTeam, TeamPIE, \
HotFuzzTeam, HotFuzzPlayer

#sample team IDs: 1610612746, 1610612760, 1610612737


#/api/search/chikagobullz/brooklennuts and spit out a winner
class NBAPredictor(Resource):
	def get(self, team1query, team2query):
		team1id = HotFuzzTeam(team1query)[2]
		team2id = HotFuzzTeam(team2query)[2]

		pie1 = TeamPIE(team1id)
		pie2 = TeamPIE(team2id)

		if pie1 == pie2:
			winner = 'TIE'
		elif pie1 > pie2:
			winner = teamdict[team1id]
		else:
			winner = teamdict[team2id]

		return jsonify({'Winner is the '+winner: {teamdict[team1id]: pie1, teamdict[team2id]: pie2}})


#get a JSON doc of all of the Teams in the NBA and all of their data
class NBATeams(Resource):
	def get(self):
		
		teams = fixer([t.__dict__ for t in Teams.query.all()])
		return jsonify({'NBA Teams': teams})


#get a JSON doc of all of the Players in the NBA and all of their data
class NBAPlayers(Resource):
	def get(self):
		players = fixer([p.__dict__ for p in Players.query.all()])
		return jsonify({'NBA Players': players})



class TeamID(Resource):
	def get(self, teamid):
		if teamid not in teamdict:
			return jsonify({'ERROR': 'ID NOT FOUND'})
		else:
			data = fixer([d.__dict__ for d in Teams.query.filter_by(TEAM_ID=teamid)])
			return jsonify({'Team ID Result': data})


class PlayerID(Resource):
	def get(self, playerid):
		if playerid not in playerdict:
			return jsonify({'ERROR': 'ID NOT FOUND'})
		else:
			data = fixer([d.__dict__ for d in Players.query.filter_by(PLAYER_ID=playerid)])
			return jsonify({'Player ID Result': data})


#Endpoints implemented for easy json lookups of teams and players via hotfuzz module
class GuessTeam(Resource):
	def get(self, teamguess):
		teamname = extractOne(teamguess, teamdict)[0]
		data = fixer([d.__dict__ for d in Teams.query.filter_by(TEAM_NAME=teamname)])
		return jsonify({teamname: data})

class GuessPlayer(Resource):
	def get(self, playerguess):
		playername = extractOne(playerguess, playerdict)[0]
		data = fixer([d.__dict__ for d in Players.query.filter_by(PLAYER_NAME=playername)])
		return jsonify({playername: data})


#return json data for all players on a specified team
class TeamPlayers(Resource):
	def get(self, teamid):
		if teamid not in teamdict:
			return jsonify({'ERROR': 'ID NOT FOUND'})
		else:
			data = PlayersInTeam(teamid)
			return jsonify({teamdict[teamid]: data})


#######################
###### ENDPOINTS ######
#######################

#main prediction engine
api.add_resource(NBAPredictor, '/hoops/<team1query>/<team2query>')


#return back a all json data for teams, players
api.add_resource(NBATeams, '/api/teams')
api.add_resource(NBAPlayers, '/api/players')

#search by teamID, playerID
api.add_resource(TeamID, '/api/teams/id/<int:teamid>')
api.add_resource(PlayerID, '/api/players/id/<int:playerid>')

#return a JSON detail of the team or player via hotfuzz 
api.add_resource(GuessTeam, '/api/teams/name/<teamguess>')
api.add_resource(GuessPlayer, '/api/players/name/<playerguess>')


#NEW - TeamPlayers
api.add_resource(TeamPlayers, '/api/teamplayers/id/<int:teamid>')

