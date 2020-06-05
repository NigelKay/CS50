import sqlite3
from cs50 import SQL

db = SQL("sqlite:///clan.db")

def updateMembers(members):
	# Set all to inactive
	db.execute("UPDATE players SET current = 0")

	for member in members:
		res = db.execute("SELECT id FROM players WHERE username = :username", username = member)

		# Create or Update
		if len(res) != 1:
			db.execute("INSERT INTO players (username, p2p, current) VALUES (:username, :p2p, :current)", username = member, p2p = 1,  current = 1)
		else:
			db.execute("UPDATE players SET current = 1 WHERE username = :username",  username = member)


def voidInactiveMembers():
	# Set the inactive players current assignments to Null
	db.execute("DELETE FROM assignments WHERE player_id IN (SELECT id FROM players WHERE current == 0)")


def updateXp(member, data):
	memberId = getMemberId(member)

	#Update the xp and level for each skill for the member
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

	# Create nested dictionary of completed status for file output
	for member in members:
		memberId = getMemberId(member)
		statusDict = {}

		mainAssignment = getCurrentMainAssignment(memberId)
		statusDict['main'] = checkTargetMet(memberId, mainAssignment)

		opAssignment = getCurrentOptionalAssignment(memberId)
		statusDict['optional'] = checkTargetMet(memberId, opAssignment)

		assignmentStatusDict[member] = statusDict

	return assignmentStatusDict


def checkTargetMet(memberId, assignment):
	# NA new members
	if assignment == None or len(assignment) < 1:
		return 'N/A'
	else:
		# Compare the new XP to the existing target
		target = assignment[0]['target_xp']
		skillId = assignment[0]['skill_id']
		targetParts = target.split()
		isLevelTarget = targetParts[0] == 'To'
		
		# Check if it is a "To level x" target, compare against level
		if isLevelTarget:
			targetLevel = int(targetParts[2])
			currentLevel = db.execute("SELECT level FROM xp WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = skillId)[0]['level']
			
			return "TRUE" if currentLevel > targetLevel else "FALSE"
		else:
			# Otherwise compare against xp
			targetXp = int(targetParts[0])
			currentXp = db.execute("SELECT xp FROM xp WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = skillId)[0]['xp']

			return "TRUE" if currentXp > targetXp else "FALSE"
			
			
def updatePreviousAssignments(members):

	# set the current months assignments to the previous month
	for member in members:
		memberId = getMemberId(member)

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


# Pick the new skills and assign their target
def createNewAssignments(members, newOptional, f2pOptional):
	for member in members:
		memberId = getMemberId(member)
		isF2p = getF2pStatus(member)

		if not isF2p:
			newMain = chooseNewMain(memberId, newOptional)
			newOpt = newOptional
		else:
			newMain = chooseNewF2pMain(memberId, f2pOptional)
			newOpt = f2pOptional

		updateMain(memberId, newMain)
		updateOptional(memberId, newOpt)


def updateMain(memberId, newMain):
	currentStatInfo = db.execute("SELECT xp, level FROM xp WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = newMain)

	preExisting = len(db.execute("SELECT player_id FROM assignments WHERE player_id = :pid AND type == 'Main'", pid = memberId)) > 0
	currentLevel = currentStatInfo[0]["level"]
	currentXp = currentStatInfo[0]["xp"]

	if currentLevel < 30:
		newTarget = "To level 30"
	elif currentLevel < 65:
		newTarget = "To level " + str(currentLevel + 1)
	else:
		newTarget = str(currentXp + 50000)

	if preExisting:
		db.execute("UPDATE assignments SET skill_id = :sid, target_xp = :xp WHERE player_id = :pid AND type == 'Main'", pid = memberId, sid = newMain, xp = newTarget)
	else:
		db.execute("INSERT INTO assignments (player_id, type, skill_id, target_xp) VALUES (:pid, 'Main', :sid, :xp)", pid = memberId, sid = newMain, xp = newTarget)


def updateOptional(memberId, newOptional):
	# TODO: Consider 200m stats
	preExisting = len(db.execute("SELECT player_id FROM assignments WHERE player_id = :pid AND type == 'Optional'", pid = memberId)) > 0
	currentXp = db.execute("SELECT xp FROM xp WHERE player_id == :pid AND skill_id == :sid", pid = memberId, sid = newOptional)[0]['xp']
	newTarget = str(currentXp + 50000)

	if preExisting:
		db.execute("UPDATE assignments SET skill_id = :sid, target_xp = :xp WHERE player_id = :pid AND type == 'Optional'", pid = memberId, sid = newOptional, xp = newTarget)
	else:
		db.execute("INSERT INTO assignments (player_id, type, skill_id, target_xp) VALUES (:pid, 'Optional', :sid, :xp)", pid = memberId, sid = newOptional, xp = newTarget)


def chooseNewMain(memberId, newOp):
	disabled = [newOp, 27]
	onetwentys = [16, 19, 20, 25, 28]

	existingMain = getCurrentMainAssignment(memberId)
	existingOptional = getCurrentOptionalAssignment(memberId)

	# Disable previous months skills from selection
	if len(existingMain) > 0:
		disabled.append(existingMain[0]['skill_id'])
	if len(existingOptional) > 0:
		disabled.append(existingOptional[0]['skill_id'])

	# Assign lowest non 99
	lowestSkillUnder99 = lowestUnder99(memberId, disabled)
	if lowestSkillUnder99 != None:
		return lowestSkillUnder99
	
	# If none under 99, assign a non maxed 120 stat
	lowestSkillUnder120 = lowestUnder120(memberId, disabled, onetwentys)
	if lowestSkillUnder120 != None:
		return lowestSkillUnder120

	# Default to lowest valid skill should the member be maxed
	return lowestSkill(memberId, disabled)


def chooseNewF2pMain(memberId, f2pOptional):
	# Exclude members skills
	disabled = [f2pOptional, 16, 17, 18, 19, 20, 22, 23, 24, 26, 27, 28]

	existingMain = getCurrentMainAssignment(memberId)
	existingOptional = getCurrentOptionalAssignment(memberId)

	if len(existingMain) > 0:
		disabled.append(existingMain[0]['skill_id'])
	if len(existingOptional) > 0:
		disabled.append(existingOptional[0]['skill_id'])

	return lowestSkill(memberId, disabled)


def getMemberId(member):
	return db.execute("SELECT id FROM players WHERE username = :username",  username = member)[0]['id']


def getF2pStatus(member):
	return db.execute("SELECT p2p FROM players WHERE username = :username",  username = member)[0]['p2p'] == 0


def getCurrentMainAssignment(memberId):
	return db.execute("SELECT skill_id, target_xp FROM assignments WHERE player_id == :pid AND type == 'Main'", pid = memberId)


def getCurrentOptionalAssignment(memberId):
	return db.execute("SELECT skill_id, target_xp FROM assignments WHERE player_id == :pid AND type == 'Optional'", pid = memberId)


def lowestUnder99(memberId, disabled):
	skillsUnder99 = db.execute("SELECT skill_id FROM xp WHERE player_id == :pid AND level < 99 ORDER BY xp ASC", pid = memberId)
	
	ids = [skills['skill_id'] for skills in skillsUnder99]
	validIds = [id for id in ids if id not in disabled]
	
	if len(validIds) > 0:
		return validIds[0]
	else:
		return None


def lowestUnder120(memberId, disabled, onetwentys):
	skillsUnder120 = db.execute("SELECT skill_id FROM xp WHERE player_id == :pid AND level < 120 ORDER BY xp ASC", pid = memberId)

	ids = [skills['skill_id'] for skills in skillsUnder120]
	onetwentyIds = [id for id in ids if id in onetwentys]
	validIds = [id for id in onetwentyIds if id not in disabled]

	if len(validIds) > 0:
		return validIds[0]
	else:
		return None


def lowestSkill(memberId, disabled):
	rankedSkills = db.execute("SELECT skill_id FROM xp WHERE player_id == :pid ORDER BY xp ASC", pid = memberId)

	ids = [skills['skill_id'] for skills in rankedSkills]
	validIds = [id for id in ids if id not in disabled]

	return validIds[0]


def getSkillNameById(id):
	return db.execute("SELECT skill_name FROM skills WHERE id == :id", id = id)
