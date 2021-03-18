import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.linalg import lu_factor, lu_solve


def inverse_exponent_method(matrix, max_iterations, sigma, eps):
    vector = np.random.randint(-1, 2, (np.shape(matrix)[0], 1))
    vector = vector / np.linalg.norm(vector)
    iterations_made = 0
    matrix = matrix - np.diag(np.full(np.shape(matrix)[0], sigma))
    lu, piv = lu_factor(matrix) #dekompozycja Lu
    #nie wiedzialem jak porownac te zbieznosci bo w 3 liczba iteracji zalezy od tego jak sigma jest blisko do danej
    #wartosci wlasnej, w 1 liczba iteracji zalezy tylko od macierzy i wektora poczatkowego i zazwyczaj
    #wychodzilo mi 6-15 iteracji
    for i in range(max_iterations):
        vector_next = lu_solve((lu, piv), vector) #rozwiazanie ukladu rownan wykorzystujac dekompozycje LU

        r = (vector_next.transpose().dot(matrix)).dot(vector_next) / (vector_next.transpose().dot(vector_next))
        print(np.linalg.norm(vector_next))
        vector_next = vector_next / np.linalg.norm(vector_next)
        tmp1 = vector_next.copy()
        tmp2 = vector.copy()
        if(np.linalg.norm(np.array(list(map(abs, tmp1))) - np.array(list(map(abs, tmp2)))) < eps):
            print("Exiting beacuse of small difference")
            iterations_made = i
            break

        vector = vector_next

    if(iterations_made == 0):
        iterations_made = max_iterations

    return iterations_made, vector_next, r


def make_symmetric(size, min, max):
    arr = np.random.randint(min, max, (size, size))
    tmp = np.tril(arr)
    arr = np.tril(tmp, -1).transpose()
    return (arr + tmp)

arr = make_symmetric(size=10, min=-6, max=20)
w, v = np.linalg.eig(arr)
v = np.array(v).transpose()
print("Eigenvals of matrix from lib")
print(w)
value = int(input("Choose sigma: "))

iterations_made, eigen_vector, r = inverse_exponent_method(matrix=arr, max_iterations=1000, sigma=value, eps=10 ** (-6))

index = 0
current = max(w)
for i in range(np.shape(arr)[0]):
    if(abs(w[i] - value) < current):
        index = i
        current = abs(w[i] - value)

print(eigen_vector.flatten(), "Eigenvector from approximation", end='\n\n')
print(v[index], "Eigenvector from lib")
print(iterations_made, "Iterations made")
print(w[index], "Eigenvalue from lib")
print(r + value, "Eigenvalue from approximation")