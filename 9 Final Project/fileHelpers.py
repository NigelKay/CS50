import csv

def writeCurrentMonth(data):
	with open('output/Current_Month_Assignments_Status.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['Username', 'Main', 'Optional'])
		for player in data:
			writer.writerow([player.replace('_', ' '), data[player]['main'], data[player]['optional']])