import random
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import plot_countour as cnt
from speed import calculate_velocity_distance
from normal import propability


def list_in_countur(contour, list_coord):
    """
    Определение колиества точек в контуре
    :param contour:
    :param list_coord:
    :return:
    """
    point_in = []
    point_number = 0

    # средняя точка рассеивания

    for point in list_coord:
        if cnt.in_contour(contour[:, 0], contour[:, 1], point[0], point[1]):
            point_in.append(point_number)
        point_number += 1

    return point_in


contour = cnt.cont
contour[:, 0] = contour[:, 0] * cnt.k_h
contour[:, 1] = contour[:, 1] * cnt.k_l

dist = 350
spread = 0.01
V = 350

propability(spread, dist, contour)


def fitness(radius, rho):
    targets = min(32 / (4 / 3) / np.pi / radius ** 2 / rho, 3 * 0.16 * 0.019 ** 2 * 0.02 / radius ** 3)
    velocity = calculate_velocity_distance(radius, rho, V, 0.5, (4 / 3) * np.pi * radius ** 2 * rho, dist, 0.1)
    energy = velocity ** 2 * (4 / 3) * np.pi * radius ** 2 * rho
    return energy * propability(spread, dist, contour) * targets, targets, velocity, energy


# Создание данных
x = np.linspace(0.002, 0.008, 10)  # Значения по оси X
y = np.linspace(2.8e3, 19.25e3, 10)  # Значения по оси Y
x, y = np.meshgrid(x, y)  # Создание сетки координатprint(type(x))# Векторизация функции
vectorized_function = np.vectorize(fitness)
z1, z2, z3, z4 = vectorized_function(x, y)  # Вычисление значений по оси Z

# Создаем фигуру с двумя трехмерными подграфиками
fig = plt.figure(figsize=(12, 12))

# Первый трехмерный график
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot_surface(x, y, z1, cmap='viridis', edgecolor='none')
ax1.set_title('Доносимая энергия')
ax1.set_xlabel('radios')
ax1.set_ylabel('rho')
ax1.set_zlabel('Плотность вероятности')

# Второй трехмерный график
ax2 = fig.add_subplot(222, projection='3d')
ax2.plot_surface(x, y, z2, cmap='plasma', edgecolor='none')
ax2.set_title('Число элементов')
ax2.set_xlabel('radios')
ax2.set_ylabel('rho')
ax2.set_zlabel('number')

# Третий трехмерный график
ax3 = fig.add_subplot(223, projection='3d')
ax3.plot_surface(x, y, z3, cmap='viridis', edgecolor='none')
ax3.set_title('Скорость')
ax3.set_xlabel('radios')
ax3.set_ylabel('rho')
ax3.set_zlabel('velosity')

# Четвертый трехмерный график
ax4 = fig.add_subplot(224, projection='3d')
ax4.plot_surface(x, y, z4, cmap='viridis', edgecolor='none')
ax4.set_title('Энергия элемента')
ax4.set_xlabel('radios')
ax4.set_ylabel('rho')
ax4.set_zlabel('Energy')

plt.tight_layout()
plt.show()
