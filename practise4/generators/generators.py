#A simple generator function
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value) 

#Generator of nums for 1 to 5
def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)

#we will create a simple generator that will yield three integers. 
#Then we will print these integers by using Python for loop.
def fun():
    yield 1            
    yield 2            
    yield 3            
 
# Driver code to check above generator function
for val in fun(): 
    print(val)

# We will create a generator object 
#that will print the squares of integers between the range of 1 to 6 (exclusive)
sq = (x*x for x in range(1, 6))
for i in sq:
    print(i)

#Generator for large sequences
def large_sequence(n):
  for i in range(n):
    yield i

# This doesn't create a million numbers in memory
gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen)) 
print(next(gen))

#Generator Expressions
gen_exp = (x * x for x in range(5))
print(gen_exp)
print(list(gen_exp)) 

# Calculate sum of squares without creating a list
total = sum(x * x for x in range(10))
print(total) 

#Generate 100 Fibonacci numbers
def fibonacci():
  a, b = 0, 1
  while True:
    yield a
    a, b = b, a + b

# Get first 100 Fibonacci numbers
gen = fibonacci()
for _ in range(100):
  print(next(gen)) 