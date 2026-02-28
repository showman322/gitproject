"""Lists, tuples, dictionaries, and sets are all iterable objects. 
They are iterable containers which you can get an iterator from.
All these objects have a iter() method which is used to get an iterator"""

#Return an iterator from a tuple, and print each value
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

#Strings are also iterable objects, containing a sequence of characters
mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#Looping Through an Iterator
mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x) 


#Iterate the characters of a string
mystr = "banana"

for x in mystr:
  print(x) 


#Create an iterator that returns numbers, starting with 1,
#and each sequence will increase by one (returning 1,2,3,4,5 etc.)
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter)) 


#StopIteration
#Stop after 20 iterations
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)