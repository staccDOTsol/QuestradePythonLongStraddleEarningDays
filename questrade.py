import requests, json
import datetime as DT
from lxml import html
import math
import os.path

today = DT.date.today()
#one_day = today + DT.timedelta(days=1) ## in production
two_days = today + DT.timedelta(days=0)
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
if os.path.isfile(two_days.strftime('%Y-%m-%d') + ".txt"):

	with open(two_days.strftime('%Y-%m-%d') + ".txt", 'r') as r:
		for line in r.readlines():
			if "," in line:
				line = line[line.index(',') + 1:]
				option1 = line[0:line.index(',')]
				line = line[line.index(',') + 1:]
				option2 = line
				uri = server + "v1/accounts/26016670/positions"
				r = requests.get(uri, headers=headers)
				response = r.json()
				#print response
				#print option1
				#print option2
				for item in response['positions']:
					#print item
					if item['symbolId'] == int(option1):
						qty1 = item['openQuantity']
					if item['symbolId'] == int(option2):
						qty2 = item['openQuantity']
				
				uri = server + "v1/accounts/26016670/orders"
				data = { 
					"accountNumber" : 26016670,
					"symbolId": int(option1),
					"quantity": qty1,
					"isAllOrNone": True,
					"isAnonymous": False,
					"orderType": "Market",
					"timeInForce": "Day",
					"action": "Sell",
					"primaryRoute": "AUTO",
					"secondaryRoute": "AUTO"
				}
				r = requests.post(uri, json=data, headers=headers)
				response1 = r.json()
				#print response1
				data = { 
					"accountNumber" : 26016670,
					"symbolId": int(option2),
					"quantity": qty2,
					"isAllOrNone": True,
					"isAnonymous": False,
					"orderType": "Market",
					"timeInForce": "Day",
					"action": "Sell",
					"primaryRoute": "AUTO",
					"secondaryRoute": "AUTO"
				}
				r = requests.post(uri, json=data, headers=headers)
				response = r.json()
				#print response

uri = server + "v1/time"
r = requests.get(uri, headers=headers)
response = r.json()
print response
earningTickers = []
eight_days_earnings = requests.get("http://www.nasdaq.com/g00/earnings/earnings-calendar.aspx?date=" + eight_days.strftime('%Y-%m-%d') + "&i10c.referrer=")
nine_days_earnings = requests.get("http://www.nasdaq.com/g00/earnings/earnings-calendar.aspx?date=" + nine_days.strftime('%Y-%m-%d') + "&i10c.referrer=")
ten_days_earnings = requests.get("http://www.nasdaq.com/g00/earnings/earnings-calendar.aspx?date=" + ten_days.strftime('%Y-%m-%d') + "&i10c.referrer=")
tree8 = html.fromstring(eight_days_earnings.content)
companies8 = tree8.xpath("//table[@id='ECCompaniesTable']//td[contains(., '(')]/a/text()")
tree9 = html.fromstring(nine_days_earnings.content)
companies9 = tree9.xpath("//table[@id='ECCompaniesTable']//td[contains(., '(')]/a/text()")
tree10 = html.fromstring(ten_days_earnings.content)
companies10 = tree10.xpath("//table[@id='ECCompaniesTable']//td[contains(., '(')]/a/text()") 
for company in companies8:
	start = company.index('(')
	start+=1
	end = company.index(')')
	earningTickers.append(company[start:end])
	with open(eight_days.strftime('%Y-%m-%d') + '.txt', 'a') as f:
		f.write(company[start:end] + '\n')
for company in companies9:
	start = company.index('(')
	start+=1
	end = company.index(')')
	earningTickers.append(company[start:end])
	with open(nine_days.strftime('%Y-%m-%d') + '.txt', 'a') as f:
		f.write(company[start:end] + '\n')
for company in companies10:
	start = company.index('(')
	start+=1
	end = company.index(')')
	earningTickers.append(company[start:end])
	with open(ten_days.strftime('%Y-%m-%d') + '.txt', 'a') as f:
		f.write(company[start:end] + '\n')
print earningTickers

uri = server + "v1/accounts/26016670/balances"
r = requests.get(uri, headers=headers)
response = r.json()
#print response
cadbuyingpower = response['perCurrencyBalances'][0]['buyingPower']
usdbuyingpower = response['perCurrencyBalances'][1]['buyingPower']

symbolIds = []

for ticker in earningTickers:
	uri = server + "v1/symbols/search?prefix=" + ticker
	r = requests.get(uri, headers=headers)
	response = r.json()
	symbolIds.append(response['symbols'][0]['symbolId'])
for symbol in symbolIds:
	uri = server + "v1/markets/quotes/" + str(symbol)
	r = requests.get(uri, headers=headers)
	response = r.json()
	price = response['quotes'][0]['lastTradePriceTrHrs']
	uri = server + "v1/markets/quotes/options"
	down = int(price)
	i = 44
	done = False
	while i <= 70 and done is not True: #70
		
 		i+=1
		date = today + DT.timedelta(days=i)
		dates = date.strftime('%Y-%m-%d')
		dates += "T00:00:00.000000-05:00" 
		#print dates
		data = {
	    "filters": [
		{
		    "optionType": "Call",
		    "underlyingId": symbol,
		    "expiryDate": dates,
		    "minstrikePrice": down,
		    "maxstrikePrice": down
		},
		{
		    "optionType": "Put",
		    "underlyingId": symbol,
		    "expiryDate": dates,
		    "minstrikePrice": down,
		    "maxstrikePrice": down
		}
	    ]
	}	
		r = requests.post(uri, json=data, headers=headers)
		response = r.json()
		#print response
		if len(response['optionQuotes']) > 1:	
			ask1 = response['optionQuotes'][0]['askPrice']
			print ask1
			ask2 = response['optionQuotes'][1]['askPrice']
			print ask2
			if ask1 is not None:
				cost = (ask1 * 100) + (ask2 * 100)
				qty = int((usdbuyingpower / 20) / cost)
				print qty 	
				option1 = response['optionQuotes'][0]['symbolId']
				option2 = response['optionQuotes'][1]['symbolId']
				done = True
				underlying = response['optionQuotes'][0]['underlying']
				#print underlying
				uri = server + "v1/accounts/26016670/orders"
				data = { 
					"accountNumber" : 26016670,
					"symbolId": option1,
					"quantity": qty,
					"isAllOrNone": True,
					"isAnonymous": False,
					"orderType": "Market",
					"timeInForce": "Day",
					"action": "Buy",
					"primaryRoute": "AUTO",
					"secondaryRoute": "AUTO"
				}
				r = requests.post(uri, json=data, headers=headers)
				response1 = r.json()
				#print response1
				data = { 
					"accountNumber" : 26016670,
					"symbolId": option2,
					"quantity": qty,
					"isAllOrNone": True,
					"isAnonymous": False,
					"orderType": "Market",
					"timeInForce": "Day",
					"action": "Buy",
					"primaryRoute": "AUTO",
					"secondaryRoute": "AUTO"
				}
				r = requests.post(uri, json=data, headers=headers)
				response = r.json()
				#print response
				with open(eight_days.strftime('%Y-%m-%d') + '.txt', 'a') as f:
				    with open(eight_days.strftime('%Y-%m-%d') + '.txt', 'r') as r:
					    for line in r.readlines():
						if line.startswith(underlying):
							f.write(underlying + "," + str(option1) + "," + str(option2) + "\n")
				with open(nine_days.strftime('%Y-%m-%d') + '.txt', 'a') as f:
				    with open(nine_days.strftime('%Y-%m-%d') + '.txt', 'r') as r:
					    for line in r.readlines():
						if line.startswith(underlying):
							f.write(underlying + "," + str(option1) + "," + str(option2) + "\n")
				with open(ten_days.strftime('%Y-%m-%d') + '.txt', 'a') as f:
				    with open(ten_days.strftime('%Y-%m-%d') + '.txt', 'r') as r:
					    for line in r.readlines():
						if line.startswith(underlying):
							f.write(underlying + "," + str(option1) + "," + str(option2) + "\n")
