#1
import math
degree = int(input())
radians = degree * math.pi/180
print(radians)

#2
h = int(input())
a = int(input())
b = int(input())
print((a+b) / 2 * h)

#3
n = int(input())
s = int(input())

area = (n * s**2) / (4 * math.tan(math.pi / n))
print(int(area))

#4
base = int(input())
height = int(input())
print(base * height)
