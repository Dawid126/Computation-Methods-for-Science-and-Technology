import numpy as np
import matplotlib.pyplot as plt

def QR_decomposition(matrix):
    size = np.shape(matrix)[0]
    Q = np.zeros((size, size))
    R = np.zeros((size,size))

    matrix = matrix.transpose()
    Q[0] = matrix[0] / np.linalg.norm(matrix[0])

    for k in range(1, size):
        sum = np.zeros((1, size))
        for i in range(k):
            sum = sum + np.dot(Q[i], matrix[k]) * Q[i]
        Q[k] = matrix[k] - sum
        Q[k] = Q[k] / np.linalg.norm(Q[k])

    for i in range(size):
        for j in range(i, size):
            R[i, j] = np.dot(Q[i], matrix[j])

    matrix = matrix.transpose()
    return Q.transpose(), R

def test_QR():
    for i in range(4):
        size = np.random.randint(1, 10, 1)[0]
        matrix = np.random.random((size, size))
        Q_library, R_library = np.linalg.qr(matrix)
        Q, R = QR_decomposition(matrix)
        print("Q, R from library")
        print(Q_library, end="\n\n")
        print(R_library, end="\n\n")
        print("Q, R from implementation")
        print(Q, end="\n\n")
        print(R)
        print("----------------------------");

def different_cond():
    matrix = np.random.random((8, 8))
    conds = []
    norms = []
    U, s, Vh = np.linalg.svd(matrix)

    for i in range(30):
        index = np.random.randint(0, 8, 1)[0]
        value = np.random.randint(100, 1000, 1)[0]
        s_copy = s.copy()
        s_copy[index] = s_copy[index] * value
        s_copy= np.diag(s_copy)
        A = np.dot(U, np.dot(s_copy, Vh))
        Ua, sa, Vha = np.linalg.svd(A)
        conds.append(sa[0] / sa[7])
        Q, R = QR_decomposition(A)
        I = np.identity(8)
        norms.append(np.linalg.norm(I - np.dot(Q.transpose(), Q)))

    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax1.plot(conds, norms, 'ro')
    ax1.set(xlabel = 'Cond(A)', ylabel = '||I - Q.transpose().dot(Q)||' ,title = "Relation between conds and norms")
    fig.savefig('conds-norms_chart' + '.png')


test_QR()
#different_cond()
