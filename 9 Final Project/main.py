import apiHelpers as highscores
import fileHelpers as files
import dal as database

# get list of members
members = ["Example"]
database.updateMembers(members)
database.voidInactiveMembers()

# record all skills and xp
for member in members:
	xpData = highscores.getData(member)
	database.updateXp(member, xpData)

# check whether previous assignment met and update
currentAssignmentsData = database.checkCurrentAssignments(members)
files.writeCurrentMonth(currentAssignmentsData)
database.updatePreviousAssignments(members)

# Get new month optional
# Consider how these will be retrieved
newOp = 17
f2pOp = 1

database.createNewAssignments(members, newOp, f2pOp)
files.writeNewAssignments(members)