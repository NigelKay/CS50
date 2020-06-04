import csv

import dal as database

def writeCurrentMonth(data):
	with open('output/Current_Month_Assignments_Status.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['Username', 'Main', 'Optional'])
		for player in data:
			writer.writerow([player.replace('_', ' '), data[player]['main'], data[player]['optional']])


def writeNewAssignments(members):
	with open("output/New_Month_Assignments.csv", 'w') as file:
		writer = csv.writer(file)
		writer.writerow(["Forum Code"])
		for member in members:
			ok = generatePasteCode(member)
			writer.writerow([ok])


def generatePasteCode(member):
	username = member.replace("_", " ")
	memberId = database.getMemberId(member)

	mainSkillInfo = database.getCurrentMainAssignment(memberId)
	OptionalSkillInfo = database.getCurrentOptionalAssignment(memberId)

	mainSkillName = database.getSkillNameById(mainSkillInfo[0]['skill_id'])[0]['skill_name']
	mainSkillTarget = formatNumber(mainSkillInfo[0]['target_xp'])

	optionalSkillName = database.getSkillNameById(OptionalSkillInfo[0]['skill_id'])[0]['skill_name']
	optionalSkillTarget = formatNumber(OptionalSkillInfo[0]['target_xp'])


	partA = "[url=https://apps.runescape.com/runemetrics/app/levels/player/" + username + "][img]http://services.runescape.com/m=avatar-rs/" + username 
	partB = "/chat.png[/img]" + username + "[/url]:[list][*][b]Main: [/b]" + mainSkillName + " " + mainSkillTarget
	partC = "[*][b]Secondary: [/b]" + optionalSkillName + " " + optionalSkillTarget + "[/list]"

	return partA + partB + partC







# 		[url=https://apps.runescape.com/runemetrics/app/levels/player/Sariou][img]http://services.runescape.com/m=avatar-rs/Sariou/chat.png[/img]Sariou[/url]:
# [list][*][b]Main: [/b]Strength No Data
# [*][b]Secondary: [/b]Slayer No Data [/list]



def formatNumber(input):
	if input.split()[0] == 'To':
		return input
	else:
		num = int(input)
		formatted = format(num, ',d')
		return str(formatted)