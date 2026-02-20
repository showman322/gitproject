#The filter() function creates a list of items for which a function returns True
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)


numbers = [ 2, 3, 4, 5, 6, 9, 12]
morethan5 = list(filter(lambda x: x > 5, numbers))
print(morethan5)

words = ["hi", "cat", "elephant", "dog"]
long_words = list(filter(lambda w: len(w) > 3, words))
print(long_words)
people = [
    {"name": "Alex", "age": 17},
    {"name": "Bob", "age": 20},
    {"name": "Chris", "age": 16}
]
adults = list(filter(lambda p: p["age"] >= 18, people))
print(adults)

words = ["hello", "", "world", "", "python"]
clean = list(filter(lambda w: w != "", words))
print(clean)

