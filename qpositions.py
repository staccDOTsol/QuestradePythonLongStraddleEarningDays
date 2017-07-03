import requests, json
import datetime as DT
from lxml import html
import math
import os.path

today = DT.date.today()
#one_day = today + DT.timedelta(days=1) ## in production
two_days = today + DT.timedelta(days=2)
eight_days = today + DT.timedelta(days=8)
nine_days = today + DT.timedelta(days=9)
ten_days = today + DT.timedelta(days=10)

with open ('refresh_token.txt', 'r') as f:
	refresh_token = f.read().strip()
response = requests.get("https://practicelogin.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=" + refresh_token)
print response.content
r = json.loads(response.content)
print r
access_token = r['access_token']
token_type = r['token_type']
server = r['api_server']
refresh_token = r['refresh_token']
with open('refresh_token.txt', 'w') as f:
	f.write(refresh_token)
headers = {'Authorization': token_type + ' ' + access_token, 'content-type': 'application/json'}
uri = server + "v1/accounts/26016670/positions"
r = requests.get(uri, headers=headers)
response = r.json()
print response
openPnl = 0
closedPnl = 0
totalCost = 0
for item in response['positions']:
	#print 'closed pnl: ' + str(item['closedPnl'])
	#print 'open pnl: ' + str(item['openPnl'])
	totalCost = totalCost + item['totalCost']
	closedPnl = closedPnl + item['closedPnl']
	openPnl = openPnl + item['openPnl']
print 'closed pnl: ' + str(closedPnl)
print 'open pnl: ' + str(openPnl)
print 'cost: ' + str(totalCost)
