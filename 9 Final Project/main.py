import apiHelpers as highscores
import fileHelpers as files
import dal as database

# get list of members
# members = ["Agile_Nigle"]
members = ["Agile_Nigle", "Greatcow", "VeraLynn", "momwuzhere", "Eramaen"]
database.updateMembers(members)
database.voidInactiveMembers()

# database.writeSkills()


# record all skills and xp
for member in members:
	xpData = highscores.getData(member)
	database.updateXp(member, xpData)

# check whether previous assignment met
currentAssignmentsData = database.checkCurrentAssignments(members)
files.writeCurrentMonth(currentAssignmentsData)

# Update PreviousAssignments
database.updatePreviousAssignments(members)

# Get new month optional
newOp = 17
f2pOp = 1

# Pick new assignments
database.createNewAssignments(members, newOp, f2pOp)

# Make file of pastable new assignments
files.writeNewAssignments(members)