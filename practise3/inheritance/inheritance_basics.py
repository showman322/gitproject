class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname() 

#To keep the inheritance of the parent's __init__() function, 
# add a call to the parent's __init__() function
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname) 

#Python also has a super() function that will make the child class 
# inherit all the methods and properties from its parent
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname) 

#Adding methods
class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear) 

#Add a PROPERTY called graduationyear to the Student class
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
    self.graduationyear = 2019

#Add a year parameter, and pass the correct year when creating objects
class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

x = Student("Mike", "Olsen", 2019) 

