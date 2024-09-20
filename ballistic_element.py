# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 08:36:26 2023

@author: RAV
"""
import numpy as np
import matplotlib.pylab as plt
from scipy.integrate import odeint

import ballistic_calc
import element as el

t = np.arange(0, 150, 0.1)
# d_ = 2.0

rho_dr = 11.35e3
rho_dr = 7.81e3

element_3 = el.Shot_element_1(0.01, 0.03, 0.003, 3)
m = element_3.volume * rho_dr
S_m = element_3.midelle_square

V = 76
theta = np.deg2rad(25)
vartheta = np.deg2rad(30)
omega_z = 5
c_x = 0.15
c_y = 0.25
l = 0.1
x_0 = [V, theta, omega_z, vartheta, 0, 0]
y = odeint(el.motion_el, x_0, t, (element_3, l))

# zero_point = np.argmax(y[:, 5] < 0)
# y = y[:zero_point, :]
# t = t[:zero_point]
zero_point = -1
y_dict = {'t': t[:zero_point],
          'V': y[:zero_point, 0],
          'theta': y[:zero_point, 1],
          'omega_z': y[:zero_point, 2],
          'vartheta': y[:zero_point, 3],
          'x': y[:zero_point, 4],
          'y': y[:zero_point, 5]}

print('Максимальная дальность ', np.max(y[:, 0]), 'Время', np.max(t))

energy_element = m * y_dict['V'] ** 2/2
# range_traj = np.sqrt(y[:, 0] ** 2 + y[:, 1] ** 2)

plt.subplot(1, 2, 1)
plt.plot(y_dict['t'], y_dict['x'], 'k', label='y')
plt.plot(y_dict['t'], y_dict['y'], '--k', label='x')
plt.title('Координаты от времени')
plt.xlabel('t, c')
plt.ylabel('x, y, м')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(y_dict['x'], y_dict['y'], 'k', )
plt.xlabel('x, м')
plt.ylabel('y, м')
plt.title('Высота от дальности')
plt.tight_layout()
plt.grid()

plt.figure()
plt.plot(y_dict['t'], energy_element, '--k', label='x')
plt.title('Кинетическая энергия')
plt.xlabel('t, c')
plt.ylabel('$E_k$, Дж')
plt.legend()
plt.grid()
plt.show()
