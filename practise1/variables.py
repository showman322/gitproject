#python variables
x = 5
y = "John"
print(x)
print(y)

x = 4       
x = "Sally" 
print(x)

x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0 

#Variable names
myvar = "Ilya"
my_var = "John"
_my_var = "Demid"
myVar = "Alex"
MYVAR = "Andrey"
myvar2 = "Fallen"

#Illegal variable names
"""
2myvar = "John"
my-var = "John"
my var = "John"
"""
#Assign multiple values
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

a = b = c = "Orange"
print(a)
print(b)
print(c)

fruits = ["apple", "banana", "cherry"]
g, d, w = fruits
print(g)
print(d)
print(w)

#Output variables
x = "Python is awesome"
print(x)
#------------------------------------
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)
#------------------------------------
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)
#------------------------------------
x = 5
y = 10
print(x + y)
#------------------------------------
x = 5
y = "John"
print(x, y)

#illegal sum of variables
x = 5
y = "John"
print(x + y)


#Global Variables
x = "awesome"

def myfunc():
  print("Python is " + x)
myfunc() 

x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x) 

