import math
import matplotlib.pyplot as plt
import numpy as np

# Общий вес заряда дроби в граммах
total_weight = 32  # граммы

# Плотность свинца в г/см³
density_lead = 11.34  # г/см³

# Индекс заполнения
packing_density = 0.64

# Радиусы дроби в мм
radii = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

# Глобальная переменная для расстояния в метрах
distance = 80  # метры

# Начальная скорость дроби в м/с
initial_velocity = 400  # м/с

# Количество серий выстрелов
num_series = 30


# Функция для вычисления массы одной дробины
def mass_of_pellet(radius_mm):
    radius_cm = radius_mm / 10  # переводим мм в см
    volume = (4 / 3) * math.pi * (radius_cm ** 3)  # объем дробины в см³
    mass = volume * density_lead  # масса дробины в граммах
    return mass / 1000  # переводим в килограммы


# Функция для вычисления разлета дроби на заданном расстоянии
def compute_spread(radius_mm, distance):
    # Простейшая модель разлета, можно усложнить по необходимости
    spread_at_distance = 0.1 * distance * 100  # разлет в см (примерная модель)
    return spread_at_distance


# Функция для вычисления скорости на заданном расстоянии
def velocity_at_distance(initial_velocity, distance):
    # Простая модель замедления (можно усложнить по необходимости)
    final_velocity = initial_velocity * (1 - 0.02) ** distance  # 2% замедление на метр
    return max(final_velocity, 0)  # скорость не может быть отрицательной


# Вычисление количества дробин для каждого радиуса
def compute_pellet_counts(radii):
    pellet_counts = {}
    total_volume = total_weight / density_lead  # общий объем заряда в см³
    for r in radii:
        mass = mass_of_pellet(r) * 1000  # масса одной дробины в граммах
        count = (packing_density * total_weight) / mass
        pellet_counts[r] = int(count)
    return pellet_counts


# Чтение контура мишени из файла
def read_contour(filename):
    contour = np.loadtxt(filename, delimiter=',')  # Указание разделителя
    return contour[:, 0], contour[:, 1]


# Центрирование контура
def center_contour(x, y):
    center_x = np.mean(x)
    center_y = np.mean(y)
    centered_x = x - center_x
    centered_y = y - center_y
    return centered_x, centered_y


# Проверка попаданий в мишень
def count_hits(x, y, path):
    points = np.vstack((x, y)).T
    hits = path.contains_points(points)
    return np.sum(hits), hits


# Построение графика средней кинетической энергии
def plot_energy(pellet_counts, distance):
    energy_series = {radius: [] for radius in pellet_counts}
    for _ in range(num_series):
        for radius, count in pellet_counts.items():
            spread = compute_spread(radius, distance)
            angles = np.random.uniform(0, 2 * np.pi, count)
            distances = np.random.uniform(0, spread / 2, count)
            final_velocity = velocity_at_distance(initial_velocity, distance)
            mass = mass_of_pellet(radius)  # масса уже в кг
            energy_per_pellet = 0.5 * mass * (final_velocity ** 2)
            total_energy = energy_per_pellet * count
            energy_series[radius].append(total_energy)

    # Усреднение результатов по сериям
    average_kinetic_energies = {radius: np.mean(energies) for radius, energies in energy_series.items()}

    # Построение графика
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_energy_graph(average_kinetic_energies, ax)
    plt.show()


# Построение графика энергии
def plot_energy_graph(kinetic_energies, ax):
    radii = list(kinetic_energies.keys())
    energies = list(kinetic_energies.values())

    ax.plot(radii, energies, marker='o')
    ax.set_title('Average Total Kinetic Energy Delivered to Target')
    ax.set_xlabel('Pellet Radius (mm)')
    ax.set_ylabel('Total Kinetic Energy (J)')
    ax.grid(True)


# Использование программы
pellet_counts = compute_pellet_counts(radii)
plot_energy(pellet_counts, distance)
