import numpy as np
from scipy import integrate

def simpson_integral(x_vector, y_vector):
    h = x_vector[1] - x_vector[0]
    n = len(x_vector)
    if(n % 2 == 0):
        print("n must be odd")
        exit(1)

    val1 = y_vector[0]
    val2 = 0
    val3 = 0
    val4 = y_vector[-1]

    k = (len(y_vector) - 1) // 2

    for i in range(1, k+1):
        val2 = val2 +  y_vector[2*i - 1]
        if(i < k):
            val3 = val3 +  y_vector[2*i]

    result = h / 3 * (val1 + 4*val2 + 2*val3 + val4)
    return result

x_vector = np.arange(0, 9)
x2 = lambda x: x**2
y_vector = list(map(x2, x_vector))
print("x ** 2")
print(f"Result from implemented func : {simpson_integral(x_vector, y_vector)}")
print(f"Result from quad from library : {integrate.quad(x2, x_vector[0], x_vector[-1])}", end = "\n\n")

x_vector = np.arange(0, 10*9 - 1)
exp = lambda x: np.exp(-x)
y_vector = list(map(exp, x_vector))
print("exp")
print(f"Result from implemented func : {simpson_integral(x_vector, y_vector)}")
print(f"Result from quad from library : {integrate.quad(exp, x_vector[0], np.inf)}")


