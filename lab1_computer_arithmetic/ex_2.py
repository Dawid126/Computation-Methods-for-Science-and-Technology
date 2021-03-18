import numpy as np
import time

# 2 Zad 1, 2, 3 ==================================

v = np.float(0.53125)
precise = np.float32(v * (10 ** 7))
tab = np.full((10**7), v, dtype=np.float32)

sum=np.float32(0.0)
err=np.float32(0.0)
y=np.float32

temp=np.float32
start = time.time()
for i in range(10**7):
    y = tab[i] - err
    temp = sum + y
    err = (temp - sum) - y
    sum = temp
end = time.time()

print("Blad bezwzgledny w Kahanie")
print(precise - sum)
print("Blad wzgledny w Kahanie")
print((precise - sum)/precise)
print(end - start)