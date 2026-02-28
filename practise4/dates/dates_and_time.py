#Import the datetime module and display the current date
import datetime

x = datetime.datetime.now()
print(x) 

#Return the year and name of weekday
import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))

#Creating Date Objects
import datetime
x = datetime.datetime(2020, 5, 17)
print(x) 

#Display the name of the month
import datetime
x = datetime.datetime(2018, 6, 1)
print(x.strftime("%B")) 

#Attributes of timedelta 
from datetime import timedelta
delta = timedelta(
    days=50,
    seconds=27,
    microseconds=10,
    milliseconds=29000,
    minutes=5,
    hours=8,
    weeks=2
)
# Only days, seconds, and microseconds remain
delta
datetime.timedelta(days=64, seconds=29156, microseconds=10)

