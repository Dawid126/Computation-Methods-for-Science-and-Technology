import numpy as np
import time
import matplotlib.pyplot as plt

#Zad 1, 2, 3 ========================================
v = np.float(0.53125)
sum=np.float32(0.0)
precise = np.float32(v * (10 ** 7))
tmp_precise = np.float32(1.0)

tab = np.full((10**7), v, dtype=np.float32)
x_axis = np.arange(25000, 10**7 + 25000, 25000)
errors = np.zeros(10**7//25000)

start = time.time()
for i in range(10**7):
   sum = sum + tab[i]
   if i % 25000 == 0 and i > 0:
       tmp_precise =np.float32(v * i)
       errors[i//25000] = np.float32((tmp_precise - sum) / tmp_precise)
end = time.time()

print("Blad bezwzgledny")
print(abs(precise - sum))
print("Blad wzgledny")
print(abs(precise - sum) / precise * 100, "%")
print("Czas trwania sumowania:", (end - start))

plt.plot(x_axis, errors, 'ro')
plt.ylabel("Blad wzgledny")
plt.xlabel("Numer iteracji")
plt.show()
# Zad 4, 5, 6 ===============================
def suma(l, r, array):
    if l==r: return array[r]

    q = (l+r)//2
    return suma(l, q, array) + suma(q+1, r, array)


start = time.time()
secondResult = suma(0, 10**7-1, tab)
end = time.time()
print("Blad bezwzgledny w rekurencyjnym")
print(abs(precise - secondResult))
print("Blad wzgledny w rekurencyjnym")
print(abs(precise - secondResult)/precise)
print("Czas trwania sumowania w rekurencyjnym")
print(end - start)



# Zad 7 ====================================

tab1 = np.arange(0.0, (10 ** 4) + 0.2, 0.2)
precise2 = np.float32((10 ** 4)/2 * len(tab1))

result2 = suma(0, len(tab1) - 1, tab1)

print("Blad wzgledny Zad 7")
print(abs(precise2 - result2))
print("Blad bezwzgledny Zad 7")
print((abs(precise2 - result2)/precise2))

