# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:24:06 2023

@author: RAV
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

v_0 = 375
h = 10
l = 50
alpha = np.arctan(h / l)
# print(np.rad2deg(alpha))
x_0 = [0, 0, v_0 * np.cos(alpha), v_0 * np.sin(alpha)]

rho_dr = 11.35e3


def mass_dr(rho_dr, d):
    d = d * 10 ** -3
    m = rho_dr * 4 / 3 * np.pi * (d / 2) ** 3

    return np.round(m, 6)


def motion_dr(x_0, t, m, S_m, c_x, c_y):
    rho = 1.22500
    # c_x= 0.25
    # c_y= 0.25
    g = 9.78

    x, y, V_x, V_y = x_0
    alpha = np.arctan(V_y / V_x)

    dx = [V_x,
          V_y,
          -(rho * V_x ** 2) / (2 * m) * S_m * c_x * np.cos(alpha),
          -(rho * V_y ** 2) / (2 * m) * S_m * c_y * np.sin(alpha) - g]

    return dx


def motion_el(x_0, t, m, S_m, c_x, c_y):
    rho = 1.22500
    g = 9.8

    J_z = 0.2

    m_z_omega = 0.2
    m_z_alpha = 0.15
    l = 0.25

    V, theta, omega_z, vartheta, x_g, y_g = x_0
    alpha = vartheta - theta

    dx = [-c_x * rho * S_m * V ** 2 / (2 * m) - g * np.sin(theta),  # dV
          c_y * rho * S_m * V * alpha / (2 * m) - g * np.cos(theta) / V,  # dtheta
          -1 / J_z * (m_z_omega * rho * S_m * l ** 2 * V * vartheta),  # d omega_z
          omega_z,
          V * np.cos(theta),
          V * np.sin(theta)]

    return dx


if __name__ == '__main__':
    t = np.arange(0, 15, 0.1)
    d_ = 2.0
    c_x = 0.5
    c_y = 0.5
    m = mass_dr(rho_dr, d_)
    S_m = np.pi * (d_ * 10 ** -3 / 2) ** 2

    v_0 = 150
    h = 20
    l = 50
    alpha = np.arctan(h / l)

    x_0 = [0, 0, v_0 * np.cos(alpha), v_0 * np.sin(alpha)]

    y = odeint(motion_el, x_0, t, (m, S_m, c_x, c_y))
    print(y)
    zero_point = np.argmax(y[:, 1] < 0)
    y = y[:zero_point, :]
    t = t[:zero_point]

    plt.subplot(1, 2, 1)
    plt.plot(t, y[:, 1], 'k', label='y')
    plt.plot(t, y[:, 0], '--k', label='x')
    plt.title('Координаты от времени')
    plt.xlabel('t, c')
    plt.ylabel('x, y, м')
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(y[:, 0], y[:, 1], 'k', )
    plt.xlabel('x, м')
    plt.ylabel('y, м')
    plt.title('Высота от дальности')
    plt.tight_layout()
    plt.grid()
    plt.show()
