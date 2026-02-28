#1
from datetime import datetime, timedelta
current_date = datetime.now()

new_date = current_date - timedelta(days = 5)

print(new_date)

#2
today = datetime.now().date()

yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#3
now = datetime.now()
wout_microsecs = now.replace(microsecond = 0)
print(wout_microsecs)

#4
date1 = datetime(2026, 2, 24, 12, 0, 0)
date2 = datetime(2026, 2, 25, 12, 0, 0)

difference = date2 - date1

print("Difference in seconds:", difference.total_seconds())
