import numpy as np

x0 = np.float32(0.6)
x1 = np.float32(0.7)
x2 = np.float32(0.8)
r = 4
eps = np.float32(1.1922e-07)

def logistic(x, r):
    return r * x * (1 - x)

x = x0
counter = 0
while (x > eps):
    new_x = logistic(x, r)
    x = new_x
    counter = counter + 1

print(x0)
print(counter)


x = x1
counter = 0
while (x > eps):
    new_x = logistic(x, r)
    x = new_x
    counter = counter + 1

print(x1)
print(counter)

x = x2
counter = 0
while (x > eps):
    new_x = logistic(x, r)
    x = new_x
    counter = counter + 1

print(x2)
print(counter)