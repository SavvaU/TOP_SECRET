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

hight_1 = 0.06
hight_2 = 0.01
radius = 0.005
el_3 = el.Shot_element_1(hight_1, hight_2, radius, 3)

c_x = 0.04
c_y = 0.5

V = 120
theta = np.deg2rad(45)
Psi = np.deg2rad(0)
omega_y = 0
omega_z = 0
x_g = 0
y_g = 0
z_g = 0
psi = np.deg2rad(0)
vartheta = np.deg2rad(45)
V_x = V * np.cos(vartheta)
V_y = V * np.sin(vartheta)
x_0 = [x_g, y_g, V_x, V_y]

y = odeint(el.motion_el_2, x_0, t, (el_3, c_y))

zero_point = np.argmax(y[:, 1] < 0)
y = y[:zero_point, :]
t = t[:zero_point]

V = np.sqrt(y[:, 2] ** 2 + y[:, 3] ** 2)

y_dict = {'t': t[:zero_point],
          'x_g': y[:zero_point, 0],
          'y_g': y[:zero_point, 1],
          'V': V[:zero_point]}

plt.subplot(1, 2, 1)
plt.plot(y_dict['t'], y_dict['y_g'], 'k', label='$y_g$')
plt.plot(y_dict['t'], y_dict['x_g'], '--k', label='$x_g$')
plt.title('Координаты от времени')
plt.xlabel('t, c')
plt.ylabel('x, y, м')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(y_dict['t'], y_dict['V'], 'k', )
plt.xlabel('t, с')
plt.ylabel('V, м/с')
plt.title('Скорость')
plt.tight_layout()
plt.grid()
plt.show()
print(np.max(y_dict['y_g']))
