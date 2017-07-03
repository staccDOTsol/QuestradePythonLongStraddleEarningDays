import requests, json
import datetime as DT
from lxml import html
import math
import os.path
import datetime
import time
server = ""
headers = {}
weekno = datetime.datetime.today().weekday()
def requestTry(i):
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
	return r			
def perCurrency():
	uri = server + "v1/accounts/26016670/balances"
	r = requests.get(uri, headers=headers)
	response = r.json()
	if 'perCurrencyBalances' in response:
		
		return response['perCurrencyBalances'][1]['buyingPower']
	else:
		print 'time.sleep60'
		time.sleep(60)
		perCurrency()
if weekno<5:
	today = DT.date.today()
	#one_day = today + DT.timedelta(days=1) ## in production
	one_day = today + DT.timedelta(days=1)
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
	i = 1
	takenUnderlyings = []
	while i<= 9:
		i+=1
		if os.path.isfile((today + DT.timedelta(days=i)).strftime('%Y-%m-%d') + ".txt"):

			with open((today + DT.timedelta(days=i)).strftime('%Y-%m-%d') + ".txt", 'r') as r:
					for line in r.readlines():
						if "," in line:
							takenUnderlyings.append(line[:line.index(',')])
							print line[:line.index(',')]
	if os.path.isfile(one_day.strftime('%Y-%m-%d') + ".txt"):

		with open(one_day.strftime('%Y-%m-%d') + ".txt", 'r') as r:
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

	usdbuyingpower = perCurrency()
	#print response
	
	symbolIds = []

	for ticker in earningTickers:	
		time.sleep(2)
		if ticker not in takenUnderlyings:
			uri = server + "v1/symbols/search?prefix=" + ticker
			r = requests.get(uri, headers=headers)
			response = r.json()
			if 'symbols' in response:
				symbolIds.append(response['symbols'][0]['symbolId'])
			else:
				print response
		else:
			print 'ticker ' + ticker + ' already taken!'
	for symbol in symbolIds:
		time.sleep(1)
		uri = server + "v1/markets/quotes/" + str(symbol)
		r = requests.get(uri, headers=headers)
		response = r.json()
		if 'quotes' in response:
			price = response['quotes'][0]['lastTradePriceTrHrs']
			uri = server + "v1/markets/quotes/options"
			down = int(price)
			i = 44
			done = False
			while i <= 70 and done is not True: #70
		
		 		i+=1
								
				try:
					response = requestTry(i).json()
				
				except ValueError as e:
					print 'time.sleep(60)'
					time.sleep(60)
					#print response
				if 'optionQuotes' in response:
					if len(response['optionQuotes']) > 1:		
						ask1 = response['optionQuotes'][0]['askPrice']
						print ask1
						ask2 = response['optionQuotes'][1]['askPrice']
						print ask2
						if ask1 is not None:
							cost = (ask1 * 100) + (ask2 * 100)
							qty = int((usdbuyingpower / 3 / 20) / cost)
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
else:
	print "it's a weekend"
