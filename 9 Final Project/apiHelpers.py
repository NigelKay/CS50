import requests

skillsMapping = ["Attack", "Defence", "Strength", "Constitution", "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting",
"Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", 
"Farming", "Runecrafting", "Hunter", "Construction", "Summoning", "Dungeoneering", "Divination", "Invention", "Archaeology"]


def getData(name):
	request = requests.get("https://secure.runescape.com/m=hiscore/index_lite.ws?player=" + name)
	requestData = request.content.decode("utf-8").split('\n')
	trimmedRequestData = requestData[1:29]

	playerStatsDictionary = {}

	for i in range(28):
		skillName = skillsMapping[i]

		currentSkill = trimmedRequestData[i].split(',')
		
		statMapping = {}
		statMapping["xp"] = currentSkill[2]
		statMapping["level"] = currentSkill[1]

		playerStatsDictionary[skillName] = statMapping

	return playerStatsDictionary