import matplotlib.pyplot as plt
import numpy as np
import copy


N = 100
ro = 0.1
MAX_ITERATIONS = 10000
t_initial = 1
QUANTITY = np.int(N * ro)
PARAM = 1
FORCE_DIST = 7

def generate(min, max, quantity):
    x_cords = np.random.uniform(min, max, quantity)
    y_cords = np.random.uniform(min, max, quantity)
    x_cords = x_cords.reshape((QUANTITY, 1))
    y_cords = y_cords.reshape((QUANTITY, 1))
    points = np.concatenate((x_cords, y_cords), axis=1)
    return points

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def energy(points):
    sum = 0
    for i in points:
        for j in points:
            if i[0] != j[0] or i[1] != j[1]:
                dist = distance((i[0], i[1]), (j[0], j[1]))
                if(dist < FORCE_DIST):
                    sum = sum - PARAM / dist
                else:
                    sum = sum + PARAM / dist
    return sum

def neighbour(points):
    i = np.int(np.random.uniform(0, QUANTITY, 1)[0])
    while(True):
        x_move = np.random.randint(-1, 2, 1)[0]
        y_move = np.random.randint(-1, 2, 1)[0]
        new_position = [points[i][0] + x_move, points[i][1] + y_move]
        if(new_position not in points and new_position[0] < N and new_position[0] > 0
        and new_position[1] < N and new_position[1] > 0):
            break

    points[i] = new_position
    return points


def P(old_points, new_points, T):
    e1 = energy(old_points)
    e2 = energy(new_points)
    if (e2 < e1):
        return 1
    else:
        return np.exp( -(e2 - e1)/T)

def temperature(iteration, option):
    if(option == 1):
        return(1 - (iteration / MAX_ITERATIONS))
    elif(option == 2):
        return(t_initial / (iteration + 1))
    elif(option == 3):
        return(t_initial / np.log(iteration + 2))


def anneal_algorithm(points, temp_option):
    best_points = copy.deepcopy(points)
    best_e = energy(points)
    T = t_initial

    old_points = copy.deepcopy(points)
    for k in range(MAX_ITERATIONS):
        new_points = neighbour(copy.deepcopy(old_points))
        rand_num = np.random.uniform(0, 1, 1)[0]
        probability = P(old_points, new_points, T)
        if (probability >= rand_num):
            old_points = copy.deepcopy(new_points)
            new_e = energy(new_points)
            if(new_e < best_e):
                best_e = new_e
                best_points = copy.deepcopy(new_points)
        T = temperature(k, temp_option)
    return best_points, best_e

def diff_energy_func():
    global PARAM
    PARAM = 0.25
    plot_result()
    PARAM = 1
    plot_result()
    PARAM = 4
    plot_result()
    PARAM = 30
    plot_result()


def diff_temp_func():
    p = generate(0, N, QUANTITY)
    print(f'Initial energy: {energy(p)}, points: {QUANTITY}, initial temp: {t_initial}')
    for i in range(10):
        new_points, be = anneal_algorithm(p, 1)
        print("End energy with 1 - iteration / max_iteration func : ", be)
    print("----")
    for i in range(10):
        new_points, be = anneal_algorithm(p, 2)
        print("End energy with t_initial / iteration func : ", be)
    print("----")
    for i in range(10):
        new_points, be = anneal_algorithm(p, 3)
        print("End energy with Boltzman func : ", be)


def plot_result():
    old_points = generate(0, N, QUANTITY)
    print(energy(old_points))
    new_points, new_e = anneal_algorithm(old_points, 2)
    print(new_e)
    old_x = [old_points[i][0] for i in range(QUANTITY)]
    old_y = [old_points[i][1] for i in range(QUANTITY)]
    new_x = [new_points[i][0] for i in range(QUANTITY)]
    new_y = [new_points[i][1] for i in range(QUANTITY)]
    fig, ax = plt.subplots()
    plt.xlim(0, N)
    plt.ylim(0, N)
    for i in old_points:
        circle = plt.Circle((i[0], i[1]), FORCE_DIST, color='b', fill=False, clip_on=True)
        ax.add_artist(circle)
    ax.plot(old_x, old_y, 'ko')
    ax.set(xlabel=f'Start energy = {energy(old_points)}',
           title=f'{QUANTITY} points, init_temp = {t_initial}')
    fig.savefig(f'start_zad2={QUANTITY}_{PARAM}.png')
    fig, ax = plt.subplots()
    plt.xlim(0, N)
    plt.ylim(0, N)
    for i in new_points:
        circle = plt.Circle((i[0], i[1]), FORCE_DIST, color='b', fill=False, clip_on=True)
        ax.add_artist(circle)
    ax.plot(new_x, new_y, 'ko')
    ax.set(xlabel=f'End energy = {new_e}',
           title=f'{QUANTITY} points, init_temp = {t_initial}')
    fig.savefig(f'end_zad2={QUANTITY}_{PARAM}.png')

#diff_temp_func()
#diff_energy_func()
#plot_result()

