import numpy as np
import main_ as dcd
from scipy.integrate import odeint
from main import list_in_countur
import plot_countour as cnt
from pprint import pformat


class Shot_element_sph():
    """
    Класс для описания ПЭ сферической формы
    """
    x_0 = 0
    y_0 = 0
    z_0 = 0

    def __init__(self, radius, rho):
        self.radius = radius
        self.rho = rho
        self.number_edge = 1
        self.midelle_square = radius * radius * np.pi
        self.volume = 4 / 3 * np.pi * radius ** 3
        self.coordinate = [0, 0, 0]
        self.mass = self.volume * self.rho
        self.c_m = [0, 0, 0]  # центр масс
        self.c_x = 0.05  # аэродинамический коэффициент c_x
        self.c_y = 0.05  # аэродинамический коэффициент c_y
        self.c_z = 0.05  # аэродинамический коэффициент c_z


def number_elements_in_diameter(R, r):
    return (int(np.floor(R / r)) * R ** 2 * 0.64) // r ** 2


def motion_el_3_simple(x_0, t, element):
    rho = 1.22500  # плотность воздуха
    g = 9.8

    V, theta, Psi, x_g, y_g, z_g = x_0

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


def calc_ballistic(t, element, x_0):
    y = odeint(motion_el_3_simple, x_0, t, args=(element,))

    zero_point = np.argmax(y[:, 4] < 0)
    y = y[:zero_point, :]
    t = t[:zero_point]

    y_dict = {'t': t,
              'V': y[:, 0],
              'theta': y[:, 1],
              'Psi': y[:, 2],
              'x_g': y[:, 3],
              'y_g': y[:, 4],
              'z_g': y[:, 5]}

    return y_dict

def calc_energy(y_dict, mass, dist):
    # dist = 100
    # время на дистанции dist, например 100 метров
    t_100 = np.interp(dist, y_dict['x_g'], y_dict['t'])

    # на дистанции 100 метров
    V_100 = np.interp(t_100, y_dict['t'], y_dict['V'])
    kinetic_energy = V_100 ** 2 * mass / 2
    return kinetic_energy

def Energy_impact(t, rho, radius, R, dist, x_0):

    global y_dict
    el_3 = Shot_element_spheric(radius,rho)
    V, theta, Psi, x_g, y_g, z_g = x_0

    # количество элементов
    N = int(number_elements_in_diameter(R, el_3.radius))
    delta = 2  # угол разлета

    list_coord = []
    list_data = []
    angls = []

    for i in range(N):
        theta = np.deg2rad(theta + delta / 2 + np.random.randn() * delta)
        Psi = np.deg2rad(delta / 2 + np.random.randn() * delta)
        angls.append([np.rad2deg(Psi), np.rad2deg(theta)])
        x_0 = [V, theta, Psi, x_g, y_g, z_g]

        y_dict = calc_ballistic(t, el_3, x_0)  # Решение ДУ !!!

        list_coord.append(dcd.calc_coord_on_dist(y_dict, dist))

        list_data.append(y_dict)

    list_coord = np.array(contour, list_coord)

    result = dict()
    result['nuber_of_shots'] = N
    result["number_of_hits"] = list_in_countur(list_coord)
    result["energy_of_each"] = calc_energy(y_dict, el_3.mass,dist)
    result["energy_impact"] = result["number_of_hits"] * result["energy_of_each"]
    return result


# Параметры линейного поиска
MIN_RAD = 10 ** -3
print(MIN_RAD)
MAX_RAD = 5 * 10 ** -3
STEP_RAD = 0.1
DIST = 100
NUMBER = 10
SPEED = [70, 100, 130, 160, 190, 210, 240, 270]

x_0 = [100, np.deg2rad(30), np.deg2rad(0), 0, 0, 0]
RHO = [11.35, 7.2, 19.25]  # допустимые дискретные значения для гена
Radius = np.arange(MIN_RAD, MAX_RAD, 2 * 10**-4)

t = np.arange(0, 20, 0.05)
R = 18.5 * 10**-3

contour = cnt.cont

contour[:, 0] = contour[:, 0] * cnt.k_h
contour[:, 1] = contour[:, 1] * cnt.k_l

results = dict()
rho_dict = dict()

for rho in RHO:
    for radius in Radius:
        results[radius] = Energy_impact(t, 11.35,  radius, R, DIST, x_0)
    rho_dict[rho] = results
    results.clear()
# Запись с использованием pprint
with open('rho.txt', 'w') as file:
    file.write(pformat(rho_dict))
