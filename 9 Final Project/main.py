import apiHelpers as highscores
import fileHelpers as files
import dal as database

# get list of members
members = ["Agile_Nigle", "Greatcow"]

database.updateMembers(members)

# database.writeSkills()


# record all skills and xp
for member in members:
	xpData = highscores.getData(member)
	database.updateXp(member, xpData)

# check whether previous assignment met
currentAssignmentsData = database.checkCurrentAssignments(members)
files.writeCurrentMonth(currentAssignmentsData)

# Update PrevAss
database.updatePreviousAssignments(members)

# Pick new assignments



# output prev assignment met status
# output print string