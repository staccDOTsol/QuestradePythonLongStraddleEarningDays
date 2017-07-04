# QuestradePythonLongStraddleEarningDays

Note that this script is now technically a strangle but by a very small bit. It looks for calls and puts within the dollar of a strikeprice in difference.

This script connects Questrade with a scraped site to see when confirmed earning days are 7-9 days out, then sees if it can find long straddle positions to buy that are 60-90 days til expiry, then opens them with Limit orders good for Day for the asking price of the calls and puts. It opens a quantity of any it finds based on a money management scheme (ie. ((buyingpower / 20) / (cost of put buy + cost of call buy))) and strives to only work on weekdays. 

Upon running the day before the earning date for that underlying, the script sells those positions.

qpositions.py outputs:

closed pnl: -34

open pnl: 653

cost: 81507

note that this script doesn't work unless you follow the directions here: 

http://www.questrade.com/api/documentation/getting-started

and paste the generated token, replacing the contents of 'refresh_token.txt.'

Also, replace every instance of '26016670' with your account # you want to work with in questrade.py and qpositions.py and qpositions/qpositionsApp/views.py.

This script works with both Questrade practice & real accounts.

Afterwards, run: 
sudo nohup quest.sh &

(alternatively to the next two steps, you can use the Django server to monitor output of current/past positions as described in the final note)
sudo nohup qtrade.sh & 

follow your earnings with:
sudo tail -f nohup.out

Note: A Django webserver exists in the directory.

python qpositions/manage.py runserver
