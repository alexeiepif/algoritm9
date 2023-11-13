#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import bisect
import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import timeit
from scipy.optimize import curve_fit


def find(a, b, len_mass):
    for i in range(len_mass):
        if b == a[i]:
            return i
    return -1


def bin_search(a, k):
    l, r = 0, len(a)
    while l < r:
        m = (l+r) // 2
        if a[m] == k:
            return m
        elif a[m] > k:
            r = m
        else:
            l = m + 1
    return -1


def find_coeffs_line(xs, ys):
    sx = sum(xs)
    stime = sum(ys)
    sx2 = sum(i**2 for i in xs)
    sxtime = sum(i*j for i, j in zip(xs, ys))
    n = len(xs)
    matrixx = [[sx2, sx], [sx, n]]
    matrixy = [[sxtime], [stime]]
    x = np.linalg.solve(matrixx, matrixy)
    return x[0][0], x[1][0]


def find_coeffs_bin(x, time):
    params, covariance = curve_fit(log_n, np.array(x), np.array(time))
    a, b = params
    return a, b


def log_n(x, a, b):
    return a * np.log(x) + b


def create_graph(b, c, namegraph, bool_l):
    plt.scatter(b, c, s=5)
    if bool_l:
        aur, bur = find_coeffs_line(b, c)
        y_line = aur * np.array(b) + bur
    else:
        aur, bur = find_coeffs_bin(b, c)
        y_line = log_n(np.array(b), aur, bur)
    plt.plot(b, y_line, color='red')
    plt.title(namegraph + " случай")
    plt.xlabel("Размер массива")
    plt.ylabel("Время работы функции")


if __name__ == '__main__':
    for namegraph in ["Средний", "Худший"]:
        x = [i for i in range(10, 10001, 10)]
        time_linear = []
        time_binary = []
        time_binary_py = []
        randmax = 1000000
        for i in x:
            rnd.seed(i)
            a = [rnd.randint(1, randmax) for j in range(i)]
            if namegraph == "Средний":
                b = a[rnd.randint(1, len(a)-1)]
            else:
                b = randmax+1

            timer_l = (timeit.timeit(lambda: find(a, b, i), number=50))/50
            time_linear.append(timer_l)

            a.sort()
            timer_bin = (timeit.timeit(lambda: bin_search(a, b), number=50))/50
            time_binary.append(timer_bin)

            timer_bin_py = (timeit.timeit(
                lambda: bisect.bisect_left(a, b), number=50))/50
            time_binary_py.append(timer_bin_py)

        # Создание графических окон
        plt.figure(namegraph + " линейный поиск")
        plt.subplots_adjust(left=0.2)

        # Создание графиков
        create_graph(x, time_linear, namegraph, True)

        plt.figure(namegraph + " бинарный поиск")
        plt.subplots_adjust(left=0.2)

        create_graph(x, time_binary, namegraph, False)

        plt.figure(namegraph + " python бин. поиск")
        plt.subplots_adjust(left=0.2)

        create_graph(x, time_binary_py, namegraph, False)
    # Показ графиков
    plt.show()
