#The sorted() function can use a lambda as a key for custom sorting

#Sort a list of tuples by the second element
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

#Sort strings by length
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

#Sort by abs value
numbers = [-10, 3, -2, 7, -5]

result = sorted(numbers, key=lambda x: abs(x))
print(result)

#Sort by second key
products = [
    {"name": "phone", "price": 500},
    {"name": "laptop", "price": 1200},
    {"name": "mouse", "price": 20}
]
cheap_first = sorted(products, key=lambda p: p["price"])
print(cheap_first)

#Sort by last letter
words = ["cat", "dog", "elephant", "bee"]

sorted_words = sorted(words, key=lambda w: w[-1])
print(sorted_words)
