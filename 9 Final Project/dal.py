import sqlite3
from cs50 import SQL

db = SQL("sqlite:///clan.db")

def updateMembers(members):
	# Set all to inactive
	db.execute("UPDATE players SET current = 0")

	for member in members:
		res = db.execute("SELECT id FROM players WHERE username = :username", username = member)

		if len(res) != 1:
			db.execute("INSERT INTO players (username, p2p, current) VALUES (:username, :p2p, :current)", username = member, p2p = 1,  current = 1)
		else:
			db.execute("UPDATE players SET current = 1 WHERE username = :username",  username = member)


# def writeSkills():
# 	skillsMapping = ["Attack", "Defence", "Strength", "Constitution", "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting",
# 					"Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", 
# 					"Farming", "Runecrafting", "Hunter", "Construction", "Summoning", "Dungeoneering", "Divination", "Invention", "Archaeology"]

# 	for skill in skillsMapping:
# 		db.execute("INSERT INTO skills (skill_name) VALUES (:skill)",  skill = skill)


def updateXp(member, data):
	memberId = db.execute("SELECT id FROM players WHERE username = :username",  username = member)[0]['id']

	for skill in data:

		skillId = db.execute("SELECT id FROM skills WHERE skill_name == :skillName", skillName = skill)[0]['id']
		xp = data[skill]['xp']
		level = data[skill]['level']

		preExisting = len(db.execute("SELECT player_id FROM xp WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = skillId)) > 0
		
		if preExisting:
			db.execute("UPDATE xp SET xp = :xp, level = :level WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = skillId, xp = xp, level = level)
		else:
			db.execute("INSERT INTO xp (player_id, skill_id, xp, level) VALUES (:pid, :sid, :xp, :level)", pid = memberId, sid = skillId, xp = xp, level = level)


def checkCurrentAssignments(members):
	assignmentStatusDict = {}

	for member in members:
		memberId = db.execute("SELECT id FROM players WHERE username = :username",  username = member)[0]['id']
		statusDict = {}

		mainAssignment = getCurrentMainAssignment(memberId)
		statusDict['main'] = checkTargetMet(memberId, mainAssignment)

		opAssignment = getCurrentOptionalAssignment(memberId)
		statusDict['optional'] = checkTargetMet(memberId, opAssignment)

		assignmentStatusDict[member] = statusDict

	return assignmentStatusDict


def checkTargetMet(memberId, assignment):
	if assignment == None or len(assignment) < 1:
		return 'N/A'
	else:
		target = assignment[0]['target_xp']
		skillId = assignment[0]['skill_id']
		targetParts = target.split()
		isLevelTarget = targetParts[0] == 'To'
		
		if isLevelTarget:
			targetLevel = int(targetParts[2])
			currentLevel = db.execute("SELECT level FROM xp WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = skillId)[0]['level']
			
			return "TRUE" if currentLevel > targetLevel else "FALSE"
		else:
			targetXp = int(targetParts[0])
			currentXp = db.execute("SELECT xp FROM xp WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = skillId)[0]['xp']

			return "TRUE" if currentXp > targetXp else "FALSE"
			
			
def updatePreviousAssignments(members):

	for member in members:
		memberId = db.execute("SELECT id FROM players WHERE username = :username",  username = member)[0]['id']

		currentMain = getCurrentMainAssignment(memberId)
		currentOptional = getCurrentOptionalAssignment(memberId)

		currentMainSkill = None
		currentOptionalSkill = None

		if len(currentMain) != 0:
			currentMainSkill = currentMain[0]['skill_id']
		if len(currentOptional) != 0:
			currentOptionalSkill = currentOptional[0]['skill_id']

		preExisting = len(db.execute("SELECT player_id FROM previous_assignments WHERE player_id = :pid", pid = memberId)) > 0

		if preExisting:
			db.execute("UPDATE previous_assignments SET previous_main = :pmain, previous_optional = :pop WHERE player_id = :pid",
						pid = memberId, pmain = currentMainSkill, pop = currentOptionalSkill)
		else:
			db.execute("INSERT INTO previous_assignments (player_id, previous_main, previous_optional) VALUES (:pid, :pmain, :pop)",
						pid = memberId, pmain = currentMainSkill, pop = currentOptionalSkill)


def getCurrentMainAssignment(memberId):
	return db.execute("SELECT skill_id, target_xp FROM assignments WHERE player_id == :pid AND type == 'Main'", pid = memberId)

def getCurrentOptionalAssignment(memberId):
	return db.execute("SELECT skill_id, target_xp FROM assignments WHERE player_id == :pid AND type == 'Optional'", pid = memberId)