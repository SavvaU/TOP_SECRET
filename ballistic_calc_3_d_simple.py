# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:24:06 2023

@author: RAV
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import element as el

t = np.arange(0, 30, 0.01)

hight_1 = 0.05
hight_2 = 0.01
radius = 0.01
el_3 = el.Shot_element_1(hight_1, hight_2, radius, 4)

# c_x = 0.14e-2
# c_y = 0.158

el_3.c_x = 0.00175973
el_3.c_y = - 3.4028E-07
el_3.c_z = - 7.5042E-07

V = 120
theta = np.deg2rad(45)
Psi = np.deg2rad(5)
# omega_x = 0
# omega_y = 0
# omega_z = 0
x_g = 0
y_g = 0
z_g = 0

vartheta = np.deg2rad(0)
psi = np.deg2rad(0)
gamma = 0

print('масса элемента {} грамм'.format(el_3.mass*1e3))

x_0 = [V, theta, Psi, x_g, y_g, z_g]

y = odeint(el.motion_el_3_simple, x_0, t, (el_3, V))

if y[-1, 4] < 0:
    zero_point = np.argmax(y[2:, 4] < 0)
else:
    zero_point = np.argmax(y[:, 4])

y = y[:zero_point, :]
t = t[:zero_point]

zero_point = -1
y_dict = {'t': t[:zero_point],
          'V': y[:zero_point, 0],
          'theta': y[:zero_point, 1],
          'Psi': y[:zero_point, 2],
          'x_g': y[:zero_point, 3],
          'y_g': y[:zero_point, 4],
          'z_g': y[:zero_point, 5]}

plt.subplot(2, 2, 1)
plt.plot(y_dict['t'], y_dict['y_g'], 'k', label='$y_g$')
plt.plot(y_dict['t'], y_dict['x_g'], '--k', label='$x_g$')
plt.title('Координаты от времени')
plt.xlabel('t, c')
plt.ylabel('x, y, м')
plt.legend()
plt.grid()

plt.subplot(2, 2, 2)
plt.plot(y_dict['t'], y_dict['z_g'], '-k', label='$z_g$')
plt.xlabel('t, с')
plt.ylabel('$z_g$, м')
plt.title('Смещение')
plt.legend()
plt.grid()

plt.subplot(2, 2, 3)
plt.plot(y_dict['t'], y_dict['V'], 'k', label='$V$')
plt.xlabel('t, с')
plt.ylabel('V, м/с')
plt.title('Скорость')
plt.tight_layout()
plt.grid()

plt.subplot(2, 2, 4)
plt.plot(y_dict['t'], np.rad2deg(y_dict['theta']), 'k', label='$\\theta$')
plt.plot(y_dict['t'], np.rad2deg(y_dict['Psi']), '--k', label='$\\Psi$')
plt.xlabel('t, с')
plt.ylabel('$\\theta, \\Psi$, рад')
plt.title('Углы $\\theta$ и $\\Psi$')
plt.legend()
plt.tight_layout()
plt.grid()


plt.show()


