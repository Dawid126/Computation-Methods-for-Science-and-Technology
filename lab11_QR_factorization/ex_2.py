import numpy as np
import matplotlib.pyplot as plt

def solve(A, y):
    eps = 10 ** (-12)
    Q, R = np.linalg.qr(A)
    b = np.dot(Q.transpose(), y)

    x = np.linalg.solve(R, b)
    for i in range(np.shape(x)[0]):
        if(abs(x[i]) <= eps):
            x[i] = 0

    return x

def make_approximation(x, y, functions):
    m = np.shape(x)[0]
    n = np.shape(functions)[0]

    y = y.reshape((np.shape(y)[0], 1))
    A = np.zeros((m, n))

    for i in range(m):
        for j in range(n):
            A[i, j] = functions[j](x[i])

    plot_x = np.linspace(-7, 7, 50)
    plot_y = np.zeros(50)
    c = solve(A, y)

    for i in range(50):
        for j in range(np.shape(functions)[0]):
            plot_y[i] = plot_y[i] + functions[j](plot_x[i]) * c[j]

    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax1.plot(x, y, 'ro', plot_x, plot_y)
    ax1.set(xlabel='x', ylabel='y', title="Input points and approximation function")
    fig.savefig('approximation' + '.png')


x = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
y = np.array([2, 7, 9, 12, 13, 14, 14, 13, 10, 8 ,4])

def fun1(x):
    return 1

def fun2(x):
    return x

def fun3(x):
    return x ** (2)

functions = [fun1, fun2, fun3]

make_approximation(x, y, functions)