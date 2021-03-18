import numpy as np

eps = 10 ** (-8)
n = 5

AB = np.random.randint(20, size=(n, n))
AB = np.array(AB, dtype = object)
LU = np.array(AB, dtype = object)
L = np.zeros((n, n), dtype = object)
U = np.zeros((n, n), dtype = object)

# scaling


def LU_dec(matrix, L, U):
    for j in range(n):
        if abs(matrix[j][j]) < eps:
            return None
        for i in range(j + 1):
            s = 0
            for k in range(i):
                s = s + matrix[i][k] * matrix[k][j]
            matrix[i][j] = matrix[i][j] - s
        for i in range(j+1, n):
            s = 0
            for k in range(j):
                s = s + matrix[i][k] * matrix[k][j]
            matrix[i][j] = (matrix[i][j] - s) / matrix[j][j]
    return matrix

print(AB)
print('')
result = LU_dec(AB, L, U)
if (result is None):
    print("Wrong input")
U = np.triu(result)
L = np.tril(result)
for i in range(n):
    L[i][i] = 1

print(L.dot(U))
print('')
print(U)
print('')
print(L)