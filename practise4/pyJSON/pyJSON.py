#Python has a built-in package called json, which can be used to work with JSON data
import json 

#Convert from JSON to Python
# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"]) 

#Convert from Python to JSON
# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y) 

#Convert Python objects into JSON strings, and print the values
print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))

#Convert a Python object containing all the legal data types
import json

x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(x))

#Use the indent parameter to define the numbers of indents
json.dumps(x, indent=4)

#Use the separators parameter to change the default separato
json.dumps(x, indent=4, separators=(". ", " = "))

#The json.dumps() method has parameters to order the keys in the result
#Use the sort_keys parameter to specify if the result should be sorted or not
json.dumps(x, indent=4, sort_keys=True)
