# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:24:06 2023

@author: RAV
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import element as el

t = np.arange(0, 30, 0.1)

hight_1 = 0.05
hight_2 = 0.01
radius = 0.01
el_3 = el.Shot_element_1(hight_1, hight_2, radius, 4)

c_x = 0.14e-2
c_y = 0.158

el_3.c_x = 0.00175973
el_3.c_y = - 3.4028E-07
el_3.c_z = - 7.5042E-07

V = 120
theta = np.deg2rad(45)
Psi = np.deg2rad(0)
omega_x = 0
omega_y = 0
omega_z = 0
x_g = 0
y_g = 0
z_g = 0

vartheta = np.deg2rad(0)
psi = np.deg2rad(0)
gamma = 0

print('масса элемента {} грамм'.format(el_3.mass*1e3))

x_0 = [V, theta, Psi, omega_x, omega_y, omega_z, x_g, y_g, z_g, vartheta, psi, gamma]

y = odeint(el.motion_el_3, x_0, t, (el_3, c_y))

if y[-1, 7] < 0:
    zero_point = np.argmax(y[2:, 7] < 0)
else:
    zero_point = np.argmax(y[:, 7])

y = y[:zero_point, :]
t = t[:zero_point]

zero_point = -1
y_dict = {'t': t[:zero_point],
          'V': y[:zero_point, 0],
          'theta': y[:zero_point, 1],
          'Psi': y[:zero_point, 2],
          'omega_x': y[:zero_point, 3],
          'omega_y': y[:zero_point, 4],
          'omega_z': y[:zero_point, 5],
          'x_g': y[:zero_point, 6],
          'y_g': y[:zero_point, 7],
          'z_g': y[:zero_point, 8],
          'vartheta': y[:zero_point, 9],
          'psi': y[:zero_point, 10],
          'gamma': y[:zero_point, 11]}

plt.subplot(3, 2, 1)
plt.plot(y_dict['t'], y_dict['y_g'], 'k', label='$y_g$')
plt.plot(y_dict['t'], y_dict['x_g'], '--k', label='$x_g$')
plt.title('Координаты от времени')
plt.xlabel('t, c')
plt.ylabel('x, y, м')
plt.legend()
plt.grid()

plt.subplot(3, 2, 2)
plt.plot(y_dict['t'], y_dict['z_g'], '-k', label='$z_g$')
plt.xlabel('t, с')
plt.ylabel('$z_g$, м')
plt.title('Смещение')
plt.legend()
plt.grid()

plt.subplot(3, 2, 3)
plt.plot(y_dict['t'], y_dict['V'], 'k', label='$V$')
plt.xlabel('t, с')
plt.ylabel('V, м/с')
plt.title('Скорость')
plt.tight_layout()
plt.grid()

plt.subplot(3, 2, 4)
plt.plot(y_dict['t'], np.rad2deg(y_dict['theta']), 'k', label='$\\theta$')
plt.plot(y_dict['t'], np.rad2deg(y_dict['vartheta']), '--k', label='$\\vartheta$')
plt.xlabel('t, с')
plt.ylabel('$\\theta, \\vartheta$, рад')
plt.title('Углы $\\theta$ и $\\vartheta$')
plt.legend()
plt.tight_layout()
plt.grid()

plt.subplot(3, 2, 5)
plt.plot(y_dict['t'], y_dict['omega_y'], 'k', label='$\\omega_y$')
plt.plot(y_dict['t'], y_dict['omega_z'], '--k', label='$\\omega_z$')
plt.xlabel('t, с')
plt.ylabel('$\\omega_y, \\omega_y$, рад')
plt.title('Уголовые скорости')
plt.legend()
plt.tight_layout()
plt.grid()

plt.subplot(3, 2, 6)
plt.plot(y_dict['t'], np.rad2deg(y_dict['psi']), 'k', label='$\\psi$')
plt.plot(y_dict['t'], np.rad2deg(y_dict['Psi']), '--k', label='$\\Psi$')
plt.xlabel('t, с')
plt.ylabel('$\\psi$, $\\Psi$, рад')
plt.title('Уголы $\\psi$ и $\\Psi$')
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()


