# QuestradePythonLongStraddleEarningDays

This script connects Questrade with a scraped site to see when confirmed earning days are 8-10 days out, then sees if it can find long straddle positions to buy that are 45-70 days til expiry, then opens them. It opens a quantity of any it finds based on a money management scheme (ie. ((buyingpower / 20) / cost of put buy + cost of call buy)) and strives to only work on weekdays. 

Upon running the day before the earning date for that underlying, the script sells those positions.

qpositions.py outputs:

closed pnl: -34
open pnl: 653
cost: 81507

note that this script doesn't work unless you follow the directions here: 

http://www.questrade.com/api/documentation/getting-started

and paste the generated token, replacing the contents of 'refresh_token.txt.'

Afterwards, run: 
sudo nohup quest.sh &
sudo nohup qtrade.sh &

follow your earnings with:
sudo tail -f nohup.out
