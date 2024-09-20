# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:27:58 2023

@author: RAV
"""
import numpy as np
import multi_angle as ma


class geom_obj():

    def __init__(self):
        # super(geom_obj, self).__init__()
        self.rho = 2000
        self.mass = self.value * self.rho
        self.J_x, self.J_y, self.J_z = self.get_J()


class Shot_element_1():
    """
    Класс для описания ПЭ каплевидной формы
    """
    x_0 = 0
    y_0 = 0
    z_0 = 0

    def __init__(self, radius, rho):
        self.radius = radius
        self.rho = rho
        self.midelle_square = self.calc_midelle_square()
        self.mass = (4/3) * np.pi * radius**2 * self.rho
        self.c_x = 0.05#self.get_c_x()  # аэродинамический коэффицент c_x
        self.c_y = 0.05#self.get_c_y()  # аэродинамический коэффицент c_y
        self.c_z = 0.05#self.get_c_y()  # аэродинамический коэффицент c_z

    def calc_midelle_square(self):
        """
        Расчет площади миделевого сечения
        :return:
        """
        return np.pi * self.radius**2

    def calc_volume(self):
        volume = self.midelle_square * self.hight_1 / 3 + self.midelle_square * self.hight_2 / 3
        return volume

    def get_element_x(self):

        return self.coordinate[:, 0]

    def get_element_y(self):

        return self.coordinate[:, 1]

    def get_element_z(self):

        return self.coordinate[:, 2]



class Shot_element_2():
    """
    Класс для описания ПЭ стреловидной формы
    """
    x_0 = 0
    y_0 = 0
    z_0 = 0

    def __init__(self, hight_1, hight_2, radius, number_edge, rho):
        self.hight_1 = hight_1
        self.hight_2 = hight_2
        self.radius = radius
        self.rho = rho#7.81e3
        self.number_edge = number_edge
        self.midelle_square = self.calc_midelle_square()
        self.volume = self.calc_volume()
        self.coordinate = self.calс_coord_element()
        self.mass = self.volume * self.rho
        self.c_m = self.get_c_m()  # центр масс
        self.J_x, self.J_y, self.J_z = self.get_J()
        self.c_x = self.get_c_x()  # аэродинамический коэффицент c_x
        self.c_y = self.get_c_y()  # аэродинамический коэффицент c_y
        self.c_z = self.get_c_y()  # аэродинамический коэффицент c_z
        self.l_d = self.get_c_m()

    def calc_midelle_square(self):
        """
        Расчет площади миделевого сечения
        :return:
        """

        if self.number_edge == 3:
            midelle_square = 3 / 4 * 3 ** 0.5 * self.radius ** 2
        elif self.number_edge == 4:
            midelle_square = 2 * self.radius ** 2
        elif self.number_edge == 6:
            midelle_square = 3 / 2 * 3 ** 0.5 * self.radius ** 2

        return midelle_square

    def calc_volume(self):
        volume = self.midelle_square * self.hight_2
        return volume

    def get_element_x(self):

        return 0

    def get_element_y(self):

        return 0

    def get_element_z(self):

        return 0

    def get_J(self):
        """
        Метод для вычисления главного момента инерции конуса по осям x и y
        Возвращает:
        J_x - главный момент инерции по оси OX
        J_y - главный момент инерции по оси OY
        J_z - главный момент инерции по оси OZ
        """
        mass = self.volume * self.rho

        J_x_1 = (3 / 10) * mass * self.radius ** 2
        J_y_1 = 3 * mass / 20 * (self.radius ** 2 + (self.hight_1 / 4) ** 2)
        J_z_1 = 3 * mass / 20 * (self.radius ** 2 + (self.hight_1 / 4) ** 2)

        J_x_2 = (3 / 10) * mass * self.radius ** 2
        J_y_2 = 3 * mass / 20 * (self.radius ** 2 + (self.hight_2 / 4) ** 2)
        J_z_2 = 3 * mass / 20 * (self.radius ** 2 + (self.hight_2 / 4) ** 2)

        J_x = J_x_1 + J_x_2
        J_y = J_y_1 + J_y_2
        J_z = J_z_1 + J_z_2

        return J_x, J_y, J_z

    def get_c_x(self):
        """
        Метод для расчета аэродинаимческого коэффициента C_x
        пока не считается
        :return:
        """
        return 0.04

    def get_c_y(self):
        """
        Метод для расчета аэродинаимческого коэффициента C_x
        пока не считается
        :return:
        """
        return 0.15

    def get_c_m(self):
        """
        Метод для расчета центра масс
        :return:
        """
        return self.hight_1 / 2


def number_elements_in_diametr(R, r, k):
    n = int(np.floor(R / r))
    number_elements = 1
    for i in range(1, n + 1):
        number_elements += k * (n - 1)

    return number_elements


def motion_el_3(x_0, t, element, c_y):
    """
    Функция - модель трехменого движения ПЭ

    :param x_0:
    :param t:
    :param element:
    :param c_y:
    :return:
    """
    rho = 1.22500  # плотность воздуха
    g = 9.8

    # m_z_omega = element.c_z * element.l_d
    # m_z_alpha = 0.35
    # m_y_beta = 0.2
    # m_y_omega = element.c_y * element.l_d
    # l = element.l_d

    V, theta, Psi, omega_x, omega_y, omega_z, x_g, y_g, z_g, vartheta, psi, gamma = x_0

    alpha = vartheta - theta
    betta = Psi - psi
    c_x_a = - 0.0017597357
    c_y_a = - 3.4028E-07

    c_x = element.c_x + c_x_a * alpha
    c_y = element.c_y + c_y_a * alpha
    c_z = c_y_a * betta
    q = rho * V ** 2 / 2  # скоростной напор
    X = c_x * element.midelle_square * q  # аэродинамическая сила лобового сопротивления
    Y = c_y * element.midelle_square * q  # аэродинамическая подъемная сила
    Z = c_z * element.midelle_square * q
    M_x = X * element.l_d
    M_y = Z * element.l_d
    M_z = Y * element.l_d

    dx = [X / element.mass - g * np.sin(theta),  # d_V
          -Y / (element.mass * V) - g * np.cos(theta) / V,  # d_theta
          -Z / (element.mass * V * np.cos(theta)),  # d_Psi
          1 / element.J_x * M_x - (element.J_z - element.J_y) * omega_y * omega_z,  # d_omega_x
          1 / element.J_y * M_y - (element.J_x - element.J_z) * omega_x * omega_z,  # d_omega_y
          1 / element.J_z * M_z - (element.J_y - element.J_x) * omega_x * omega_y,  # d_omega_z
          V * np.cos(theta) * np.cos(Psi),  # d_x
          V * np.sin(theta),  # d_y
          V * np.cos(theta) * np.sin(Psi),  # d_z
          omega_x * np.sin(gamma) + omega_z * np.cos(gamma),  # d_vartheta
          1 / np.cos(vartheta) * (omega_y * np.cos(gamma) - omega_z * np.sin(gamma)),  # d_psi
          omega_x - np.tan(vartheta) * (omega_y * np.cos(gamma) - omega_z * np.sin(gamma))]  # d_gamma

    return dx


def motion_el_3_simple(x_0, t, element, V):
    """
    Функция - модель трехменого движения ПЭ

    :param x_0:
    :param t:
    :param element:
    :param c_y:
    :return:
    """
    rho = 1.22500  # плотность воздуха
    g = 9.8

    V, theta, Psi, x_g, y_g, z_g = x_0

    # alpha = vartheta - theta
    # betta = Psi - psi
    # c_x_a = - 0.0017597357
    # c_y_a = - 3.4028E-07

    c_x = element.c_x
    c_y = element.c_y
    c_z = element.c_y
    q = rho * V ** 2 / 2  # скоростной напор
    X = c_x * element.midelle_square * q  # аэродинамическая сила лобового сопротивления
    Y = c_y * element.midelle_square * q  # аэродинамическая подъемная сила
    Z = c_z * element.midelle_square * q * np.sin(Psi)

    dx = [X / element.mass - g * np.sin(theta),  # d_V
          -Y / (element.mass * V) - g * np.cos(theta) / V,  # d_theta
          -Z / (element.mass * V * np.cos(theta)),  # d_Psi
          V * np.cos(theta) * np.cos(Psi),  # d_x
          V * np.sin(theta),  # d_y
          V * np.cos(theta) * np.sin(Psi)]  # d_z

    return dx


def motion_el_2(x_0, t, element, c_y):
    rho = 1.22500
    g = 9.78

    x, y, V_x, V_y = x_0
    alpha = np.arctan(V_y / V_x)

    dx = [V_x,  # d_x
          V_y,  # d_y
          -(rho * V_x ** 2) / (2 * element.mass) * element.midelle_square * element.c_x * np.cos(alpha),  # d_V_x
          -(rho * V_y ** 2) / (2 * element.mass) * element.midelle_square * element.c_y * np.sin(alpha) - g]  # d_V_y

    return dx


def motion_el_3_new(x_0, t, element, c_array):
    g = 9.8
    rho = 1.225

    # theta = np.deg2rad(30)
    # phi = np.deg2rad(0)
    # psi = np.deg2rad(0)
    # V = 100

    d = 0.02
    # Аэродинамические коэффициенты
    # c_d = 0.12
    # c_y_beta = 2.5
    # c_l_alpha = 2.5
    # C_l_p = 1.8
    # c_m_alpha = 2.2
    # c_n_beta = 2.2
    # C_m_q = -500
    # C_n_r = -500
    c_d, c_y_beta, c_l_alpha, C_l_p, c_m_alpha, c_n_beta, C_m_q, C_n_r = c_array

    # C_B_LL = [[np.cos(theta) * np.cos(psi), np.sin(phi) * np.sin(theta) * np.cos(psi) - np.cos(theta) * np.sin(psi),
    #            np.sin(phi) * np.sin(psi) + np.cos(phi) * np.sin(theta) * np.cos(psi)],
    #           [np.cos(theta) * np.sin(psi), np.cos(theta) * np.cos(psi) + np.sin(phi) * np.sin(theta) * np.sin(psi),
    #            np.cos(phi) * np.sin(theta) * np.sin(psi) - np.sin(phi) * np.cos(psi)],
    #           [-np.sin(theta), np.sin(phi) * np.cos(theta), np.cos(phi) * np.cos(theta)]]

    # u = V * np.cos(theta)
    # v = 0
    # w = V * np.sin(theta)

    p, q, r, psi, theta, phi, u, v, w, x_b, y_b, z_b = x_0

    V = np.sqrt(u ** 2 + v ** 2 + w ** 2)
    Q = 0.5 * rho * V ** 2

    if w == 0:
        alpha = 0
    else:
        # alpha = 1 / np.tan(w / u)
        alpha = np.arcsin(w / V)

    if v == 0:
        beta = 0
    else:
        beta = 1 / np.tan(v / u)

    C_x = -c_d
    C_y = c_y_beta * beta
    C_z = - c_l_alpha * alpha

    C_l = C_l_p * d * p / (2 * V)
    C_m = c_m_alpha * alpha + C_m_q * d * q / (2 * V)
    C_n = c_n_beta * beta + C_n_r * d * r / (2 * V)

    F_x = C_x * Q * element.midelle_square
    F_y = C_y * Q * element.midelle_square
    F_z = C_z * Q * element.midelle_square

    M_x = C_l * Q * element.midelle_square * d
    M_y = C_m * Q * element.midelle_square * d
    M_z = C_n * Q * element.midelle_square * d

    d_x = [M_x / element.J_x,  # dot_p
           (M_y + (element.J_z - element.J_x) * p * r) / element.J_y,  # dot_q
           (M_z + (element.J_x - element.J_y) * p * q) / element.J_z,  # dot_r

           q * np.sin(phi) / np.cos(theta) - r * np.cos(phi) / np.cos(theta),  # dot_psi
           q * np.cos(phi) - r * np.cos(phi),  # dot_theta
           p + q * np.tan(theta) * np.sin(phi) + r * np.tan(theta) * np.cos(phi),  # dot_phi

           r * v - q * w - g * np.sin(theta) + F_x,  # dot_u
           p * w - r * u + g * np.cos(theta) * np.sin(phi) + F_y,  # dot_v
           q * u - p * v + g * np.cos(theta) * np.cos(phi) + F_z,  # dot_w

           u * np.cos(psi) * np.cos(theta) + v * np.sin(psi) * np.cos(theta) - w * np.sin(theta),  # d_x_b
           u * (np.sin(phi) * np.sin(theta) * np.cos(psi) - np.sin(psi) * np.cos(phi)) +
           v * (np.sin(phi) * np.sin(psi) * np.sin(theta) + np.cos(phi) * np.cos(theta)) +
           w * np.sin(phi) * np.cos(theta),  # d_y_b
           u * (np.sin(phi) * np.sin(psi) + np.sin(theta) * np.cos(phi) * np.cos(psi)) +
           v * (-np.sin(phi) * np.cos(theta) + np.sin(psi) * np.sin(theta) * np.cos(phi)) + w * np.cos(
               phi) * np.cos(theta)]  # d_z_b

    return d_x


class geom():
    def __init__(self):
        self.lengt = 1
        self.radius = 1
        self.value = self.get_value()

    def get_value(self):
        return self.radius ** 2 * np.pi


if __name__ == '__main__':

    # Определение условия плотности заполнения
    for n in range(3, 10):
        alpha = 180 - 360 / n
        gamma = 360 - alpha
        if gamma / alpha % 1 == 0:
            print('Число сторон', str(n))

    hight_1 = 0.03
    hight_2 = 0.01
    radius = 0.01
    el_3 = Shot_element_1(hight_1, hight_2, radius, 3)
    print(el_3.mass)
    el_4 = Shot_element_1(hight_1, hight_2, radius, 4)
    print(el_4.mass)
    el_6 = Shot_element_1(hight_1, hight_2, radius, 6)
    print(el_6.mass)

    number_elements = number_elements_in_diametr(0.038 / 2, 0.0025, 6)
    print('number_elements', number_elements)
