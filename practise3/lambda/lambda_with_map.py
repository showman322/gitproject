#The map() function applies a function to every item in an iterable\
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled) #double all numbers in the list

numbers = [1, 2, 3]
result = list(map(lambda x: x + 10, numbers))
print(result)

numbers = [2, 3, 4]
squares = list(map(lambda x: x ** 2, numbers))
print(squares)

numbers = [1, 2, 3]
strings = list(map(lambda x: str(x), numbers))
print(strings)

words = ["cat", "elephant", "hi"]
lengths = list(map(lambda w: len(w), words))
print(lengths)

words = ["hello", "python"]
upper = list(map(lambda w: w.upper(), words))
print(upper)