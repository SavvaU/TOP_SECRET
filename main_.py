# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:24:06 2023

Проверка правильности баллистических расчтеов
@author: RAV
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import element as el
import plot_countour as cnt


def calc_ballistic(t, element, x_0):
    c_x = 0.18
    y = odeint(el.motion_el_3_simple, x_0, t, (element, c_x))

    zero_point = np.argmax(y[:, 4] < 0)
    y = y[:zero_point, :]
    t = t[:zero_point]

    y_dict = {'t': t[:zero_point],
              'V': y[:zero_point, 0],
              'theta': y[:zero_point, 1],
              'Psi': y[:zero_point, 2],
              'x_g': y[:zero_point, 3],
              'y_g': y[:zero_point, 4],
              'z_g': y[:zero_point, 5]}

    return y_dict


def calc_energy(y_dict, mass, dist):
    # dist = 100
    # время на дистанции dist, например 100 метров
    t_100 = np.interp(dist, y_dict['x_g'], y_dict['t'])

    # на дистанции 100 метров
    V_100 = np.interp(t_100, y_dict['t'], y_dict['V'])
    kinetic_energy = V_100 ** 2 * mass / 2
    return kinetic_energy

def calc_velocity(y_dict, dist):
    # dist = 100
    # время на дистанции dist, например 100 метров
    t_dist = np.interp(dist, y_dict['x_g'], y_dict['t'])

    # на дистанции 100 метров
    V_dist = np.interp(t_dist, y_dict['t'], y_dict['V'])

    return V_dist

def calc_coord_on_dist(y_dict, dist):
    """
    Определение координат на заданной дистанции
    :param y_dict: словарь с временными рядами
    :param dist: заданная дистанция
    :return: координаты y и z на заданной дистанции
    """
    if 'x_g' in y_dict and len(y_dict['x_g']) > 0:
        if dist > np.max(y_dict['x_g']):
            return 0, 0  # Если dist больше максимального значения x_g, возвращаем (0, 0)
        else:
            # Интерполяция времени t на заданной дистанции
            t_dist = np.interp(dist, y_dict['x_g'], y_dict['t'])
            # Интерполяция координат y и z по времени
            y_dist = np.interp(t_dist, y_dict['t'], y_dict['y_g'])
            z_dist = np.interp(t_dist, y_dict['t'], y_dict['z_g'])
            return y_dist, z_dist
    else:
        return 0, 0  # В случае отсутствия данных возвращаем (0, 0)

if __name__ == '__main__':
    # контур БпЛА
    contour = cnt.cont
    contour[:, 0] = contour[:, 0] * cnt.k_h
    contour[:, 1] = contour[:, 1] * cnt.k_l

    t = np.arange(0, 150, 0.01)
    hight_1 = 0.04
    hight_2 = 0.01
    radius = 0.005
    el_3 = el.Shot_element_2(hight_1, hight_2, radius, 6)

    V = 100
    theta = np.deg2rad(30)
    Psi = np.deg2rad(0)
    omega_x = 0
    omega_y = 0
    omega_z = 0
    x_g = 0
    y_g = 0
    z_g = 0
    psi = np.deg2rad(0)
    vartheta = np.deg2rad(30)
    gamma = 0

    x_0 = [V, theta, Psi, omega_x, omega_y, omega_z, x_g, y_g, z_g, vartheta, psi, gamma]
    # количество элементов
    N = el.number_elements_in_diametr(19 * 1e-3, el_3.radius, el_3.number_edge)
    # N = 96  # количество элементов
    delta = 2  # угол разлета
    dist = 10
    list_coord = []
    list_data = []
    angls = []

    for i in range(N):
        vartheta = np.deg2rad(30)
        theta = np.deg2rad(30 + delta / 2 + np.random.randn() * delta)

        psi = np.deg2rad(0)
        Psi = np.deg2rad(delta / 2 + np.random.randn() * delta)

        angls.append([np.rad2deg(Psi), np.rad2deg(theta)])

        x_0 = [V, theta, Psi, x_g, y_g, z_g]

        y_dict = calc_ballistic(t, el_3, x_0)
        list_coord.append(calc_coord_on_dist(y_dict, dist))
        list_data.append(y_dict)
    angls = np.array(angls)
    list_coord = np.array(list_coord)

    point_in = []
    point_number = 0

    # средняя точка рассеивания
    y_mean = np.mean(list_coord[:, 0])
    z_mean = np.mean(list_coord[:, 1])

    contour[:, 0] = contour[:, 0] + y_mean
    contour[:, 1] = contour[:, 1] + z_mean

    for point in list_coord:
        if cnt.in_contour(contour[:, 0], contour[:, 1], point[0], point[1]):
            point_in.append(point_number)
        point_number += 1

    print("Количество элементов={}, радиус ПЭ={}мм, длина ПЭ={}мм".format(N, el_3.radius * 1e3,
                                                                          (el_3.hight_1 + el_3.hight_2) * 1e3))
    print("Попало {} ПЭ, масса ПЭ={} г, 'энергия одного ПЭ={} Дж".format(len(point_in),
                                                                         np.round(el_3.mass * 1e3, 1),
                                                                         calc_energy(y_dict, el_3.mass, dist)))

    # i = 0
    # for j in list_data[:10]:
    #     plt.plot(j['t'], j['y_g'], label='$\\psi$ =' + str(np.round(angls[i][0], 1)))
    #     i += 1

    # plt.legend()
    # plt.grid()

    plt.figure('point')
    plt.plot(list_coord[:, 0], list_coord[:, 1], '*')
    plt.plot(y_mean, z_mean, 'or')

    plt.xlabel('y, м')
    plt.ylabel('z, м')
    plt.plot(contour[:, 0], contour[:, 1])

    plt.grid()
    plt.show()
