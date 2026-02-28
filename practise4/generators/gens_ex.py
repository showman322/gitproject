#1
def square(n):
    for i in range(n + 1):
        yield i**2

n = int(input())
for i in square(n):
    print(i)

#2
def even_nums(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input())
for i in even_nums(n):
    print(i)

#3
def div_3_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
for i in div_3_4(n):
    print(i)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i**2

a = int(input())
b = int(input())
for x in squares(a, b):
    print(x)

#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())
for num in countdown(n):
    print(num)
