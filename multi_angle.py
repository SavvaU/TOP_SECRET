# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:13:24 2023

@author: RAV
"""
import numpy as np
import matplotlib.pyplot as plt


def current_azimuth(x1, y1, x2, y2):
    """функция для вычисления угла (азимута) на точку. задача решается на плоскости
    x1,y1  -координаты первой точки
    x2,y2 - координаты второй точки
    """
    azimuth = np.arctan2((y2 - y1), (x2 - x1))

    return azimuth


def current_length(x1, y1, x2, y2):
    """функция для вычисления расстояния между точками. задача решается на плоскости
    x1,y1  -координаты первой точки
    x2,y2 - координаты второй точки
    """
    length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return length


def new_point(x_0, y_0, angle, r):
    number_rounds = 5
    x_1 = x_0 + r * np.cos(angle)
    y_1 = y_0 + r * np.sin(angle)
    return np.round(x_1, number_rounds), np.round(y_1, number_rounds)


def calc_manyangle(x_0, y_0, r, n):
    polygon = []
    angle = 0  # начальный угол

    one_angle = np.deg2rad(360 / n)
    x_k, y_k = x_0, y_0

    for i in range(n):
        polygon.append([x_0, y_0])
        x1, y1 = new_point(x_0, y_0, angle, r)
        angle += one_angle
        x_0 = x1
        y_0 = y1

    polygon.append([x_k, y_k])
    polygon = np.array(polygon)
    x_centroid = np.mean(polygon[:-1, 0])
    y_centroid = np.mean(polygon[:-1, 1])

    polygon[:, 0] = polygon[:, 0] - x_centroid
    polygon[:, 1] = polygon[:, 1] - y_centroid
    return polygon


if __name__ == "__main__":
    x_0, y_0 = 0, 0
    r = 1
    polygon = calc_manyangle(x_0, y_0, r, 6)

    plt.plot(polygon[:, 0], polygon[:, 1])
    plt.plot(np.mean(polygon[:-1, 0]), np.mean(polygon[:-1, 1]), 'ro')
    plt.grid()
    plt.show()
