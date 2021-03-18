import matplotlib.pyplot as plt
import numpy as np

r_tab = [3.75, 3.76, 3.77, 3.78, 3.79, 3.80]

def logistic(x, r):
    return np.float32(r * x * (1 - x))

def plot_for_offset_s(r, y_max):
    t = np.arange(0.0, 100, 1)
    s = np.empty(100, dtype=np.float32)
    x = np.float32(0.7)
    s[0] = x
    for j in range(99):
        new_x = logistic(x, np.float32(r))
        s[j+1] = new_x
        x = new_x

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, s)
    ax.grid()
    ax.set(xlabel=f'n, r = {r}', ylabel='xn',
           title='Odwzorowanie logistyczne')
    ax.set_ylim(0, y_max)
    fig.savefig(f's_r={r}.png')

def plot_for_offset_d(r, y_max):
    t = np.arange(0.0, 100, 1)
    s = np.empty(100, dtype=np.float64)
    x = np.float64(0.7)
    s[0] = x
    for j in range(99):
        new_x = logistic(x, r)
        s[j+1] = new_x
        x = new_x

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, s)
    ax.grid()
    ax.set(xlabel=f'n, r = {r}', ylabel='xn',
           title='Odwzorowanie logistyczne')
    ax.set_ylim(0, y_max)
    fig.savefig(f'd_r={r}.png')

for r in r_tab:
    plot_for_offset_s(r, 1)
    plot_for_offset_d(r, 1)