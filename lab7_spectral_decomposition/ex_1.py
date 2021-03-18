import numpy as np
import matplotlib.pyplot as plt
import time


def exponent_method(matrix, max_iterations, eps):
    vector = np.random.randint(-4, 5, (np.shape(matrix)[0], 1))
    vector = vector / np.linalg.norm(vector)
    iterations_made = 0
    eigen_value = 0

    for i in range(max_iterations):
        vector_next = matrix.dot(vector)

        eigen_value = np.linalg.norm(vector_next)

        vector_next = vector_next / np.linalg.norm(vector_next)
        tmp1 = vector_next.copy()
        tmp2 = vector.copy()
        if (np.linalg.norm(np.array(list(map(abs, tmp1))) - np.array(list(map(abs, tmp2)))) < eps): #jesli wektor
            iterations_made = i # ma czesc wartosci ujemnych, to z kazda iteracja wartosci wektora zmieniaja znaki na
            break               #przeciwne, zatem przed policzeniem roznicy wykonuje abs na kazdym elemencie.
                                #gdy po prostu odejmowalem wektory to algorytm wykonywal maksymalna liczbe iteracji
        vector = vector_next    #chociaz wartosci wektora co do wartosci bezwzglednej nie zmienialy sie

    if(iterations_made == 0):
        iterations_made = max_iterations

    return iterations_made, eigen_value, vector_next


def make_symmetric(size, min, max):
    arr = np.random.randint(min, max, (size, size))
    tmp = np.tril(arr)
    arr = np.tril(tmp, -1).transpose()
    return (arr + tmp)


def compare_results(eigen_vector, eigen_value, iterations_made, arr):
    w, v = np.linalg.eig(arr)
    v = np.array(v).transpose()
    vector_lib = v[0]

    tmp1 = eigen_vector.copy()
    tmp1 = np.array(list(map(abs, tmp1)))
    counter = 0

    for vector in v:
        tmp2 = vector.copy()
        tmp2 = np.array(list(map(abs, tmp2)))
        if (np.linalg.norm(tmp1 - tmp2) < 10 ** (-3)):
            vector_lib = vector
            break

        counter = counter + 1

    print(iterations_made, f"Iterations made, shape = {np.shape(arr)[0]}")
    print(eigen_vector, "Eigenvector from approximation", end='\n\n')
    print(np.array(vector_lib), "Eigenvector from lib", end='\n\n')
    print(eigen_value, "Eigenvalue from approximation")
    print(w[counter], "Eigenvalue from lib")


shapes = np.arange(20, 6000, 200)
times = np.zeros(len(shapes))
iterations = np.zeros(len(shapes))
counter = 0

for shape in shapes:
    arr = make_symmetric(size=shape, min=-6, max=20)
    start = time.time()
    iterations_made, eigen_value, eigen_vector = exponent_method(matrix=arr, max_iterations=100, eps=10 ** (-6))
    end = time.time()
    eigen_vector = eigen_vector.flatten()
    times[counter] = end - start
    iterations[counter] = iterations_made
    counter = counter + 1

    if(counter < 5):
        compare_results(eigen_vector, eigen_value, iterations_made, arr)

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(shapes, times, 'ro')
ax1.set(xlabel="Rozmiar macierzy", ylabel="Czas", title='Porownanie czasow')
fig.savefig('times_zad1.png')

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(shapes, iterations, 'ro')
ax1.set(xlabel="Rozmiar macierzy", ylabel="Liczba wykonanych iteracji", title='Porownanie liczby wykonanych iteracji')
fig.savefig('iterations_zad1.png')



