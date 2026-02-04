thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x) #Loop through the set, and print the values:

  thisset = {"apple", "banana", "cherry"}
print("banana" in thisset) 

thisset = {"apple", "banana", "cherry"}
print("banana" not in thisset) 

#Add Set Items
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset) 

thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset) 

thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]
thisset.update(mylist)
print(thisset) #The object in the update() method does not have to be a set, it can be any iterable object (tuples, lists, dictionaries etc.).

#Remove Set Items
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana")
print(thisset) 

thisset = {"apple", "banana", "cherry"}
thisset.discard("banana")
print(thisset) 

thisset = {"apple", "banana", "cherry"}
x = thisset.pop()
print(x)
print(thisset) 

thisset = {"apple", "banana", "cherry"}
thisset.clear()
print(thisset) 

thisset = {"apple", "banana", "cherry"}
del thisset #The del keyword will delete the set completely:

#Loop Sets
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x) #Loop through the set, and print the values:

#Join Sets
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = set1.union(set2)
print(set3) #The union() method returns a new set with all items from both sets.

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = set1 | set2
print(set3) #You can use the | operator instead of the union() method, and you will get the same result.

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = {"John", "Elena"}
set4 = {"apple", "bananas", "cherry"}
myset = set1.union(set2, set3, set4)
print(myset) #Join multiple sets with the union() method:

et1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = {"John", "Elena"}
set4 = {"apple", "bananas", "cherry"}
myset = set1 | set2 | set3 |set4
print(myset) 

x = {"a", "b", "c"}
y = (1, 2, 3)
z = x.union(y)
print(z) #Join a set with a tuple:

set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}
set1.update(set2)
print(set1) #The update() method inserts the items in set2 into set1:

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1.intersection(set2)
print(set3) #The intersection() method will return a new set, that only contains the items that are present in both sets.

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set1.intersection_update(set2)
print(set1) 

set1 = {"apple", 1,  "banana", 0, "cherry"}
set2 = {False, "google", 1, "apple", 2, True}
set3 = set1.intersection(set2)
print(set3) #Join sets that contains the values True, False, 1, and 0, and see what is considered as duplicates:

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1.difference(set2)
print(set3) #The difference() method will return a new set that will contain only the items from the first set that are not present in the other set.

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1 - set2
print(set3) 
#The - operator only allows you to join sets with sets, and not with other data types like you can with the difference() method.

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set1.difference_update(set2)
print(set1)
#Use the difference_update() method to keep only the items from the first set that are not present in the other set:

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1.symmetric_difference(set2)
print(set3) 
#Keep the items that are not present in both sets:

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1 ^ set2
print(set3) #Use ^ to join two sets:

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set1.symmetric_difference_update(set2)
print(set1) 
#Use the symmetric_difference_update() method to keep the items that are not present in both sets:

#Frozenset
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))

