#add to __init__.py: 
#from hoopsapp.hoops import teamdict, playerdict, fixer, PlayersInTeam, TeamPIE...

from hoopsapp import Teams, Players, extractOne

#helpful to have these in memory to quickly lookup a player or team name
teamdict = dict(Teams.query.with_entities(Teams.TEAM_ID, Teams.TEAM_NAME))
playerdict = dict(Players.query.with_entities(Players.PLAYER_ID, Players.PLAYER_NAME))

def fixer(data):
    for item in data:
        if item['_sa_instance_state']:
            del item['_sa_instance_state']
        elif item['_labels']:
            del item['_labels']
    return data


def PlayersInTeam(teamid):
    return fixer([d.__dict__ for d in Players.query.filter_by(TEAM_ID=teamid)])


#this basically averages the PIE value for each participating player on the team
#the PIE value is what determines the winner
#This must be changed to recognize starting lineup data... 
def TeamPIE(teamid):

    teamdata = PlayersInTeam(teamid)
    #first we use map to get a list of just PIE values
    #then we use list comprehension to leave just the non-zero values
    teampie = [x for x in list(map(lambda k: k['PIE'], teamdata)) if x>0.0]

    #we calculate the resulting average and get the PIE percentage
    return float(sum(teampie)) / len(teampie) * 100


#helper functions to tap into hotfuzz 
def HotFuzzTeam(teamguess):
    #returns a tuple, index [0] is for teamname, index [2] is for teamID
    return extractOne(teamguess, teamdict)
    
    #return fixer([d.__dict__ for d in Teams.query.filter_by(TEAM_NAME=teamname)])

def HotFuzzPlayer(playerguess):
    #returns a tuple, index [0] is for playername, index [2] is for playerID
    return extractOne(playerguess, playerdict)    
