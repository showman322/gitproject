#A function with one argument
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus") 

#Parameters vs Arguments
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument 

#This function expects 2 arguments, and gets 2 arguments
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes") 

#Default Parameter Values
def my_function(name = "friend"):#"friend" is a default value
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus") 

def my_function(country = "Norway"):
  print("I am from", country)

my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil") 

#Keyword Arguments
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)#order doesn't matter

my_function(animal = "dog", name = "Buddy")

#Positinal Arguments
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function("dog", "Buddy") #Positional arguments must be in the correct order

def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function("Buddy", "dog") #Switching the order changes the result

#Passing different Data Types
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"] #list
my_function(my_fruits) 

def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25} #dictionary
my_function(my_person) 


#To specify positional-only arguments, add , / after the arguments
def my_function(name, /):
  print("Hello", name)

my_function("Emil")

#To specify that a function can have only keyword arguments, add *, before the arguments
def my_function(*, name):
  print("Hello", name)

my_function(name = "Emil") 


def my_function(name):
  print("Hello", name)
my_function("Emil") 

#Combining Positional-Only and Keyword-Only
def my_function(a, b, /, *, c, d):#Arguments before / are positional-only
  return a + b + c + d #and arguments after * are keyword-only

result = my_function(5, 10, c = 15, d = 20)
print(result) 