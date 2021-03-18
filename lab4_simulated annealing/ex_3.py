import numpy as np
import copy
import random
import matplotlib.pyplot as plt

MAX_ITERATIONS = 10000
t_initial = 0.5


def energy(state):
    matrix, _ = state
    result = 0
    for i in range(9):
        if (np.unique(matrix[i, :]).size == 9):
            result = result + 1
        if (np.unique(matrix[:, i]).size == 9):
            result = result + 1
    for i in range(3):
        for j in range(3):
            if (np.unique((matrix[i*3: (i+1)*3,j*3: (j+1)*3]).flatten()).size == 9):
                result = result + 1

    return -result


def neighbour(state):
    matrix, modifiable = state

    x, y = random.choice([(x, y) for x in [0, 3, 6] for y in [0, 3, 6]])
    coords_in_square = [m for m in modifiable if m[0] >= x and m[0] < x + 3 and m[1] >= y and m[1] < y + 3]
    coord1, coord2 = random.sample(coords_in_square, 2)

    matrix[coord1], matrix[coord2] = matrix[coord2], matrix[coord1]

    return (matrix, modifiable)


def P(old_state, new_state, T):
    e1 = energy(old_state)
    e2 = energy(new_state)
    if (e2 < e1):
        return 1
    else:
        return np.exp( -(e2 - e1)/T)


def temperature(iteration):
    return (t_initial / (iteration + 1))


def anneal(state):
    best_state = copy.deepcopy(state)
    best_e = energy(state)
    t = t_initial

    old_state = copy.deepcopy(state)
    for k in range(MAX_ITERATIONS):
        new_state = neighbour(copy.deepcopy(old_state))
        rand_num = np.random.random()
        probability = P(old_state, new_state, t)

        if probability > rand_num:
            old_state = copy.deepcopy(new_state)
            new_e = energy(new_state)
            if (new_e < best_e):
                best_e = new_e
                best_state = copy.deepcopy(new_state)
                if best_e == -27:
                    break

        t = temperature(k)
    return best_state[0], best_e


def show(state):
    if type(state) == tuple:
        modifiable = state[1]
        state = state[0]
    else:
        modifiable = []
    print("-" * (9 * 3 + 1), end="\n")

    for row in range(9):
        print('|', end='')
        for col in range(9):
            sep = "|" if col % 3 == 2 else " "
            mark = "_" if (row, col) in modifiable else " "
            print(f'{mark}{state[row, col]}', end=sep)
        print()
        if row % 3 == 2:
            print("-" * (9 * 3 + 1))


def load_sudoku():
    f = open('sudoku1.ssv', 'r+')
    arr = []
    for line in f.readlines():
        arr.append([])
        for i in line.split():
            arr[-1].append(int(i))

    f.close()
    arr = np.array(arr)
    arr = arr.reshape((9,9))
    modifiable = []
    for x in range(9):
        for y in range(9):
            if (arr[x, y] == 0):
                modifiable.append((x, y))

    for x, y in modifiable:
        cx, cy = x // 3 * 3, y // 3 * 3
        avail = [x for x in range(1, 10) if x not in arr[cx:cx + 3, cy:cy + 3]]
        arr[x, y] = random.choice(avail)

    return arr, modifiable


arr, modifiable = state = load_sudoku()
def diagram():
    iterations = np.arange(0, 10001, 100)
    energies = []
    for i in iterations:
        MAX_ITERATIONS = i
        result, e = anneal(state)
        energies.append(27 + e)

    fig, ax = plt.subplots()
    ax.plot(iterations, energies, 'o')
    fig.savefig(f'zad3_energy_diagram.png')


result, e = anneal(state)
print(e)
show((arr, modifiable))
show((result, modifiable))