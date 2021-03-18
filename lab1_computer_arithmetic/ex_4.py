import matplotlib.pyplot as plt
import numpy as np
import imageio

def logistic(x, r):
    return r * x * (1 - x)

def plot_for_offset(r, y_max):
    t = np.arange(0.0, 100, 1)
    s = []
    x = 0.7
    s.append(x)
    for j in range(99):
        new_x = logistic(x, r)
        s.append(new_x)
        x = new_x

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(t, s)
    ax.grid()
    ax.set(xlabel=f'n, r = {r}', ylabel='xn',
           title='Odwzorowanie logistyczne')

    ax.set_ylim(0, y_max)


    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image

kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave('./zbieznosc.gif', [plot_for_offset(i/100, 1) for i in range(400)], fps=20)