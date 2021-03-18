import numpy as np


# 3 Suma Riemanna, sumowanie w przod, pojedyncza precyzja
rieman_sum = np.float32(0.0)
k_to_power = np.float32(1.0)
s_tab = np.array([2, 3.6667, 5, 7.2, 10], dtype=np.float32)
n_tab = np.array([50, 100, 200, 500, 1000])
tab_length = len(s_tab) * len(n_tab)
forward_sum = np.empty(tab_length, dtype=np.float32)
backward_sum = np.empty(tab_length, dtype=np.float32)


counter = 0
for s in s_tab:
    for n in n_tab:
        for k in range(1, n+1):
            tmp_k = np.float32(k)
            k_to_power = tmp_k ** s
            rieman_sum = rieman_sum + 1 / k_to_power
        forward_sum[counter] = rieman_sum
        counter = counter +1
        rieman_sum = 0

# Suma Riemanna, sumowanie w tyl, pojedyncza precyzja

counter = 0
for s in s_tab:
    for n in n_tab:
        for k in reversed(range(1, n+1)):
            tmp_k = np.float32(k)
            k_to_power = tmp_k ** s
            rieman_sum = rieman_sum + 1 / k_to_power
        backward_sum[counter] = rieman_sum
        counter = counter +1
        rieman_sum = 0

counter = 0
for s in s_tab:
    for n in n_tab:
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w przod", forward_sum[counter])
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w tyl  ", backward_sum[counter])
        counter = counter + 1

# 3 Suma Dirichleta, sumowanie w przod, pojedyncza precyzja

forward_sum = np.empty(tab_length, dtype=np.float32)
backward_sum = np.empty(tab_length, dtype=np.float32)
counter = 0

for s in s_tab:
    for n in n_tab:
        for k in range(1, n+1):
            tmp_k = np.float32(k)
            k_to_power = tmp_k ** s
            if k % 2 == 0:
                k_to_power = (-1) * k_to_power
            rieman_sum = rieman_sum + 1 / k_to_power
        forward_sum[counter] = rieman_sum
        counter = counter +1
        rieman_sum = 0

# Suma Dirichleta, sumowanie w tyl, pojedyncza precyzja

counter = 0
for s in s_tab:
    for n in n_tab:
        for k in reversed(range(1, n+1)):
            tmp_k = np.float32(k)
            k_to_power = tmp_k ** s
            if k % 2 == 0:
                k_to_power = (-1) * k_to_power
            rieman_sum = rieman_sum + 1 / k_to_power
        backward_sum[counter] = rieman_sum
        counter = counter +1
        rieman_sum = 0

counter = 0
for s in s_tab:
    for n in n_tab:
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w przod", forward_sum[counter])
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w tyl  ", backward_sum[counter])
        counter = counter + 1
