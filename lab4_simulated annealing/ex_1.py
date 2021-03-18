import matplotlib.pyplot as plt
import numpy as np
import imageio
import copy

MIN = 0
MAX = 15
QUANTITY = 18
MAX_ITERATIONS = 10000
t_initial = 1

def generate(min, max, quantity, option):
    x_cords = []
    y_cords = []
    if (option == 1):
        x_cords = np.random.uniform(min, max, quantity)
        y_cords = np.random.uniform(min, max, quantity)
    elif(option == 2):
        x_tmp = np.random.normal(max / 4, max / 6, quantity // 4)
        y_tmp = np.random.normal(max / 4, max / 6, quantity // 4)
        x_cords = np.concatenate((x_cords, x_tmp), axis=None)
        y_cords = np.concatenate((y_cords, y_tmp), axis=None)
        x_tmp = np.random.normal(max / 2 + max / 4, max / 9, quantity // 4)
        y_tmp = np.random.normal(max / 4, max / 9, quantity // 4)
        x_cords = np.concatenate((x_cords, x_tmp), axis=None)
        y_cords = np.concatenate((y_cords, y_tmp), axis=None)
        x_tmp = np.random.normal(max / 2 + max / 4, max / 12, quantity // 4)
        y_tmp = np.random.normal(max / 2 + max / 4, max / 12, quantity // 4)
        x_cords = np.concatenate((x_cords, x_tmp), axis=None)
        y_cords = np.concatenate((y_cords, y_tmp), axis=None)
        x_tmp = np.random.normal(max / 4, max / 15, quantity // 4 + quantity % 4)
        y_tmp = np.random.normal(max / 2 + max / 4, max / 15, quantity // 4 + quantity %4)
        x_cords = np.concatenate((x_cords, x_tmp), axis=None)
        y_cords = np.concatenate((y_cords, y_tmp), axis=None)
    elif(option == 3):
        for k in range(QUANTITY):
                i = np.int(np.random.uniform(0, 3, 1)[0])
                j = np.int(np.random.uniform(0, 3, 1)[0])
                x_tmp = np.random.uniform(min + i * max / 3, max / 6 + i * max / 3, 1)
                y_tmp = np.random.uniform(min + j * max / 3, max /6 + j * max / 3, 1)
                x_cords = np.concatenate((x_cords, x_tmp), axis=None)
                y_cords = np.concatenate((y_cords, y_tmp), axis=None)
    return x_cords, y_cords


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def energy(x_array, y_array):
    sum = 0
    for i in range(QUANTITY - 1):
        sum = sum + distance((x_array[i], y_array[i]), (x_array[i+1], y_array[i+1]))
    sum = sum + distance((x_array[QUANTITY-1], y_array[QUANTITY-1]), (x_array[0], y_array[0]))
    return sum

def neighbour(x_array, y_array, option):
    i = np.int(np.random.uniform(0, QUANTITY, 1)[0])
    if(option == 1):
        if (i == QUANTITY - 1):
            x_array[i], x_array[0] = x_array[0], x_array[i]
            y_array[i], y_array[0] = y_array[0], y_array[i]
        else:
            x_array[i], x_array[i+1] = x_array[i+1], x_array[i]
            y_array[i], y_array[i+1] = y_array[i+1], y_array[i]
    else:
        j = np.int(np.random.uniform(0, QUANTITY, 1)[0])
        x_array[i], x_array[j] = x_array[j], x_array[i]
        y_array[i], y_array[j] = y_array[j], y_array[i]

    return x_array, y_array

def P(old_x_array, old_y_array, new_x_array, new_y_array, T):
    e1 = energy(old_x_array, old_y_array)
    e2 = energy(new_x_array, new_y_array)
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


def anneal_algorithm(x_array, y_array, neighbour_option, temp_option, gif_option):
    best_x = x_array.copy()
    best_y = y_array.copy()
    best_e = energy(x_array, y_array)
    if(gif_option == 1):
        images = np.array([make_one_image(x_array, y_array, best_e, t_initial)])
    T = t_initial


    old_x = x_array.copy()
    old_y = y_array.copy()
    for k in range(MAX_ITERATIONS):
        new_x, new_y = neighbour(copy.deepcopy(old_x), copy.deepcopy(old_y), neighbour_option)
        rand_num = np.random.uniform(0, 1, 1)[0]
        probability = P(old_x, old_y, new_x, new_y, T)
        if (probability >= rand_num):
            old_x = copy.deepcopy(new_x)
            old_y = copy.deepcopy(new_y)
            new_e = energy(new_x, new_y)
            if(new_e < best_e):
                best_e = new_e
                best_x = copy.deepcopy(new_x)
                best_y = copy.deepcopy(new_y)
                if(gif_option == 1):
                    images.resize((len(images) + 1, 700, 700, 3))
                    images[len(images) - 1] = make_one_image(best_x, best_y, best_e, t_initial)
    T = temperature(k, temp_option)
    if(gif_option == 1):
        return best_e, images
    else:
        return best_x, best_y, best_e


def different_temp_func():
    a, b = generate(MIN, MAX, QUANTITY, 1)
    e = energy(a, b)
    print(f'Initial energy: {e}, points: {QUANTITY}, initial temp: {t_initial}')
    for i in range(10):
        x, y ,be = anneal_algorithm(a, b, 1, 1, 0)
        print("End energy with 1 - iteration / max_iteration func : ", be)
    print("----")
    for i in range(10):
        x, y ,be = anneal_algorithm(a, b, 1, 2, 0)
        print("End energy with t_initial / iteration func : ", be)
    print("----")
    for i in range(10):
        x, y ,be = anneal_algorithm(a, b, 1, 3, 0)
        print("End energy with Boltzman func : ", be)


def arbitrary_vs_consecutive():
    a, b = generate(MIN, MAX, QUANTITY, 1)
    e = energy(a, b)
    print(f'Initial energy: {e}, points: {QUANTITY}, initial temp: {t_initial}')
    for i in range(10):
        x, y ,be = anneal_algorithm(a, b, 1, 2, 0)
        print("End energy with consecutive func : ", be)
    print("----")
    for i in range(10):
        x, y ,be = anneal_algorithm(a, b, 2, 2, 0)
        print("End energy with arbitrary func : ", be)

def plot_result():
    a, b = generate(MIN, MAX, QUANTITY, 3)
    e = energy(a, b)
    best_x = a
    best_y = b
    best_e = e
    for i in range(10):
        x, y, be = anneal_algorithm(a, b, 2, 2, 0)
        if(be < best_e):
            best_x = x.copy()
            best_y = y.copy()
            best_e = be

    fig, ax = plt.subplots(figsize=(7, 7))
    a = np.concatenate((a, a[0]), axis=None)
    b = np.concatenate((b, b[0]), axis=None)
    ax.plot(a, b, '-bo')
    ax.set(xlabel=f'Start energy = {e}',
           title=f'{QUANTITY} points, init_temp = {t_initial}')
    fig.savefig(f'zad1_3_start_n={QUANTITY}.png')

    fig, ax = plt.subplots(figsize=(7, 7))
    best_x = np.concatenate((best_x, best_x[0]), axis=None)
    best_y = np.concatenate((best_y, best_y[0]), axis=None)
    ax.plot(best_x, best_y, '-bo')
    ax.set(xlabel=f'End energy = {best_e}',
           title=f'{QUANTITY} points, init energy = {e} '
                 f'init_temp = {t_initial}')
    fig.savefig(f'zad1_3_end_n={QUANTITY}.png')


def make_one_image(x_array, y_array, energy, T):
    fig, ax = plt.subplots(figsize=(7, 7))
    x_array = np.concatenate((x_array, x_array[0]), axis=None)
    y_array = np.concatenate((y_array, y_array[0]), axis=None)
    ax.plot(x_array, y_array, '-bo')
    ax.set(xlabel=f'Energy = {energy}',
           title=f'Temperature = {T}')

    ax.set_ylim(0, MAX)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


def make_gif():
    a, b = generate(MIN, MAX, QUANTITY, 3)
    e = energy(a, b)
    best_e = e
    best_images = []
    for i in range(10):
        be, images = anneal_algorithm(a, b, 2, 2, 1)
        if (be < best_e):
            best_e = be
            best_images = images.copy()
    print(np.shape(best_images[0]))

    imageio.mimsave('./func_minim_visual.gif', best_images, fps=1)

make_gif()
#plot_result()
#arbitrary_vs_consecutive()
#different_temp_func()

