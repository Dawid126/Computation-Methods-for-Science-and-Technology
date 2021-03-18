import matplotlib.pyplot as plt
import numpy as np

r_tab = np.arange(2.5, 4, 0.01)
x = 0.8

def logistic(x, r):
    return r * x * (1 - x)


fig, ax1 = plt.subplots(figsize=(19.20, 10.80))
for r in r_tab:
    for i in range(1000):
        new_x = logistic(x, r)
        if i >= (900):
            ax1.plot(r, x, 'ko', markersize = 3)
        x = new_x


ax1.set_xlim(2.5, 4)
ax1.set_title("Bifurcation diagram")
plt.show()
fig.savefig('bifurcation_diagram.png')