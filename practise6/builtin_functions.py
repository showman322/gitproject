#MAP
numbers = [1, 2, 3, 4, 5]

result = map(lambda x: x * 2, numbers)

print(list(result))

#FILTER
numbers = [1, 2, 3, 4, 5, 6]

evens = filter(lambda x: x % 2 == 0, numbers)

print(list(evens))

#REDUCE
from functools import reduce

numbers = [1, 2, 3, 4, 5]

total = reduce(lambda x, y: x + y, numbers)

print(total)

#ENUMIRATE and ZIP
names = ["Alice", "Bob", "Charlie"]

for index, name in enumerate(names):
    print(index, name)

#-------------------------------------
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

for name, score in zip(names, scores):
    print(name, score)