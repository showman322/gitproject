#arithmetic operators
x = 15
y = 4

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y)
print(x ** y)
print(x // y)

#assignment opertors
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")
print(x:=3)

#comparison operators 
x = 5
y = 3

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

#logical operators
x = 5
print(x > 0 and x < 10)#Test if a number is greater than 0 and less than 10

x = 5
print(not(x > 3 and x < 10))#Reverse the result with not

x = 5
print(x < 5 or x > 10)#Test if a number is less than 5 or greater than 10

#Identity operators
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x
print(x is z)
print(x is y)
print(x == y)
"""
    is - Checks if both variables point to the same object in memory
    == - Checks if the values of both variables are equal
"""
x = ["apple", "banana"]
y = ["apple", "banana"]
print(x is not y)

#membership operators
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)

fruits = ["apple", "banana", "cherry"]
print("pineapple" not in fruits)

text = "Hello World"
print("H" in text)
print("hello" in text)
print("z" not in text)

#Bitwise operators
print(6 & 3) 
"""
The & operator compares each bit and set it to 1 if both are 1, otherwise it is set to 0
The binary representation of 6 is 0110
The binary representation of 3 is 0011
Then the & operator compares the bits and returns 0010, which is 2 in decimal.
"""

print(6 | 3)
"""The binary representation of 6 is 0110
The binary representation of 3 is 0011
Then the | operator compares the bits and returns 0111, which is 7 in decimal.
"""

print(6 ^ 3)
"""The ^ operator compares each bit and set it to 1 if only one is 1, otherwise (if both are 1 or both are 0) it is set to 0
The binary representation of 6 is 0110
The binary representation of 3 is 0011
Then the ^ operator compares the bits and returns 0101, which is 5 in decimal."""

#Operator precedence
"""() 	          Parentheses 	
** 	          Exponentiation 	
+x  -x  ~x    Unary plus, unary minus, and bitwise NOT 	
*  /  //  %   Multiplication, division, floor division, and modulus 	
+  - 	      Addition and subtraction 	
<<  >> 	      Bitwise left and right shifts 	
& 	          Bitwise AND 	
^ 	          Bitwise XOR 	
| 	          Bitwise OR 	
==  !=  >  >=  <  <=  is  is not  in  not in  	Comparisons, identity, and membership operators 	
not 	      Logical NOT 	
and 	      AND 	
or 	          OR"""