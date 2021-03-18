import numpy as np
import xlwt
from xlwt import Workbook

rieman_sum = np.float64(0.0)
k_to_power = np.float64(1.0)
s_tab = np.array([2, 3.6667, 5, 7.2, 10], dtype=np.float64)
n_tab = np.array([50, 100, 200, 500, 1000])
tab_length = len(s_tab) * len(n_tab)
forward_sum = np.empty(tab_length, dtype=np.float64)
backward_sum = np.empty(tab_length, dtype=np.float64)

wb = Workbook()
sheets = []


def sheet_init(name):

    sheet = wb.add_sheet(name)

    sheet.write(0, 0, 'Wartość s')
    sheet.write(0, 1, 'ζ w przód ')
    sheet.write(0, 2, 'ζ w tył')
    sheet.write(0, 3, 'η w przód')
    sheet.write(0, 4, 'η w tył')
    for i in range(5):
        sheet.write(i + 1, 0, s_tab[i])
    return sheet

# 3 Suma Riemanna, sumowanie w przod, podwojna precyzja

counter = 0
counter_excel = 0
i = 0
for n in n_tab:
    sheets.append(sheet_init(str(n)))
    for s in s_tab:
        for k in range(1, n+1):
            tmp_k = np.float64(k)
            k_to_power = tmp_k ** s
            rieman_sum = rieman_sum + 1 / k_to_power
        forward_sum[counter] = rieman_sum
        sheets[i].write(counter_excel + 1, 1, rieman_sum)
        counter = counter +1
        counter_excel = counter_excel + 1
        rieman_sum = 0
    i = i + 1
    counter_excel = 0


# Suma Riemanna, sumowanie w tyl, podwojna precyzja

counter = 0
i = 0
for n in n_tab:
    for s in s_tab:
        for k in reversed(range(1, n+1)):
            tmp_k = np.float64(k)
            k_to_power = tmp_k ** s
            rieman_sum = rieman_sum + 1 / k_to_power
        backward_sum[counter] = rieman_sum
        sheets[i].write(counter_excel + 1, 2, rieman_sum)
        counter = counter +1
        counter_excel = counter_excel + 1
        rieman_sum = 0
    i = i + 1
    counter_excel = 0

counter = 0
for n in n_tab:
    for s in s_tab:
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w przod, podwojna precyzja ", forward_sum[counter])
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w tyl, podwojna precyzja   ", backward_sum[counter])
        counter = counter + 1

# 3 Suma Dirichleta, sumowanie w przod, podwojna precyzja

forward_sum = np.empty(tab_length, dtype=np.float64)
backward_sum = np.empty(tab_length, dtype=np.float64)

counter = 0
i = 0
for n in n_tab:
    for s in s_tab:
        for k in range(1, n+1):
            tmp_k = np.float64(k)
            k_to_power = tmp_k ** s
            if k % 2 == 0:
                k_to_power = (-1) * k_to_power
            rieman_sum = rieman_sum + 1 / k_to_power
        forward_sum[counter] = rieman_sum
        sheets[i].write(counter_excel + 1, 3, rieman_sum)
        counter = counter +1
        counter_excel = counter_excel + 1
        rieman_sum = 0
    i = i + 1
    counter_excel = 0


# Suma Dirichleta, sumowanie w tyl, podwojna precyzja

counter = 0
i = 0
for n in n_tab:
    for s in s_tab:
        for k in reversed(range(1, n+1)):
            tmp_k = np.float64(k)
            k_to_power = tmp_k ** s
            if k % 2 == 0:
                k_to_power = (-1) * k_to_power
            rieman_sum = rieman_sum + 1 / k_to_power
        backward_sum[counter] = rieman_sum
        sheets[i].write(counter_excel + 1, 4, rieman_sum)
        counter = counter +1
        counter_excel = counter_excel + 1
        rieman_sum = 0
    i = i + 1
    counter_excel = 0

wb.save('podwojna_precyzja.xls')

counter = 0
for n in n_tab:
    for s in s_tab:
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w przod, podwojna precyzja ", forward_sum[counter])
        print(f's = {s}, n = {n},', "Wartosc funkcji dla sumowania w tyl, podwojna precyzja   ", backward_sum[counter])
        counter = counter + 1