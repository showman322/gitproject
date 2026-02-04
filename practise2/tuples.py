thistuple = ("apple", "banana", "cherry")
print(thistuple)

thistuple = ("apple", "banana", "cherry", "apple", "cherry")
print(thistuple) #Tuples allow duplicate values:

thistuple = ("apple", "banana", "cherry")
print(len(thistuple)) #Print the number of items in the tuple:

thistuple = ("apple",)
print(type(thistuple))

#NOT a tuple
thistuple = ("apple")
print(type(thistuple)) #One item tuple, remember the comma:

tuple1 = ("apple", "banana", "cherry")
tuple2 = (1, 5, 7, 9, 3)
tuple3 = (True, False, False) #String, int and boolean data types:

mytuple = ("apple", "banana", "cherry")
print(type(mytuple))

#Update Tuples
x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)

print(x) #Convert the tuple into a list to be able to change it:

thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.append("orange")
thistuple = tuple(y) #Convert the tuple into a list, add "orange", and convert it back into a tuple:

thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.remove("apple")
thistuple = tuple(y) #Convert the tuple into a list, remove "apple", and convert it back into a tuple:

"""thistuple = ("apple", "banana", "cherry")
del thistuple
print(thistuple) #this will raise an error because the tuple no longer exists""" 

#unpack Tuples
fruits = ("apple", "banana", "cherry") #Packing a tuple:

fruits = ("apple", "banana", "cherry")

(green, yellow, red) = fruits

print(green)
print(yellow) #Unpacking a tuple:
print(red)

fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")

(green, yellow, *red) = fruits

print(green)
print(yellow) #Assign the rest of the values as a list called "red":
print(red)

fruits = ("apple", "mango", "papaya", "pineapple", "cherry")

(green, *tropic, red) = fruits

print(green)
print(tropic) #Add a list of values the "tropic" variable:
print(red)

#Loop Tuples
thistuple = ("apple", "banana", "cherry")
for x in thistuple:
  print(x) 

thistuple = ("apple", "banana", "cherry")
for i in range(len(thistuple)): #Use the range() and len() functions to create a suitable iterable.
  print(thistuple[i])

thistuple = ("apple", "banana", "cherry")
i = 0
while i < len(thistuple):
  print(thistuple[i])
  i = i + 1 

#Join Tuples
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3) 

fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2

print(mytuple) #Multiply the fruits tuple by 2:
