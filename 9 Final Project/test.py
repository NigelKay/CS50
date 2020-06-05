import requests

mydata = requests.get("https://secure.runescape.com/m=hiscore/index_lite.ws?player=Agile_Nigle")

print(mydata.content)