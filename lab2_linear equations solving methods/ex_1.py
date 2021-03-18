import numpy as np
import time

eps = 10 ** (-8)
k = 500
l = 501

AB = np.random.randint(20, size=(k, l))
AB = np.array(AB, dtype = object)
A = np.array(AB[:, :-1], dtype=float)
B = np.array(AB[:, -1], dtype=float)
#print(AB)

def find_max_row_value(matrix, ind):
    max = matrix[ind][ind]
    index = ind
    for row in range(ind, k):
        if matrix[row][ind] > max:
            max = matrix[row][ind]
            index = row
    return index


# partial pivoting and solving the equation
def gaussian(matrix, k, l):
    for i in range(0, k):
        max_value_index = find_max_row_value(matrix, i)
        matrix[[i, max_value_index]] = matrix[[max_value_index, i]]
        coeff_1 = matrix[i][i]
        for row in range(0, k):

            if row != i:
                if abs(coeff_1) > eps:
                    coeff_2 = matrix[row][i] / matrix[i][i]
                    for column in range(0, l):
                        tmp = coeff_2 * matrix[i][column]
                        matrix[row][column] = matrix[row][column] - tmp
                matrix[row][i] = 0
    for i in range(0, k):
        if abs(matrix[i][i]) > eps:
            matrix[i][l - 1] = matrix[i][l - 1] / matrix[i][i]
            matrix[i][i] = 1
    return matrix


start = time.time()
# scaling
max = AB[0][0]
for row in range(0, k):
    for column in range(0, l):
        if max < AB[row][column]:
            max = AB[row][column]
    for column in range(0, l):
        AB[row][column] = AB[row][column] / max

res1 = gaussian(AB,k,l)
stop = time.time()
print("Czas liczenia:", stop-start)

start = time.time()
res2 = np.linalg.lstsq(A, B)
stop = time.time()
print("Czas liczenia przy pomocy bibliotek numpy:", stop-start)


#for i in range(k):
#    for j in range(l):
#        print(res1[i][j], end=' ')
#    print('')

#print(res2)