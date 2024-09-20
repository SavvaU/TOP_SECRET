import numpy as np
import matplotlib.pyplot as plt


def calculate_velocity_distance(r, rho, v0, Cx, m, dist, dt=0.5):
    """
    Рассчитывает зависимость скорости сферы от пройденного расстояния.

    Аргументы:
    r : float
        Радиус сферы в метрах.
    rho : float
        Плотность воздуха в кг/м^3.
    v0 : float
        Начальная скорость в м/с.
    Cx : float
        Коэффициент лобового сопротивления для сферы.
    m : float
        Масса сферы в кг.
    dt : float, optional
        Шаг интегрирования по времени в секундах (по умолчанию 0.01 с).

    Возвращает:
    distance : numpy.ndarray
        Массив пройденных расстояний в метрах.
    velocity : numpy.ndarray
        Массив скоростей сферы на соответствующих пройденных расстояниях в м/с.
    """
    rho = 1.74
    # Создаем массивы для хранения данных
    time = [0.0]  # время
    velocity = [v0]  # скорость
    distance = [0.0]  # пройденное расстояние
    # Цикл по времени для численного интегрирования
    while distance[-1] < dist:
        # Сила сопротивления воздуха
        Fd = 0.5 * Cx * rho * np.pi * r ** 2 * velocity[-1] ** 2

        # Ускорение
        acceleration = -Fd / m * 10

        # Изменение скорости и расстояния по методу Эйлера
        new_velocity = velocity[-1] + acceleration * dt
        new_distance = distance[-1] + velocity[-1] * dt

        # Обновляем данные
        time.append(time[-1] + dt)
        velocity.append(new_velocity)
        distance.append(new_distance)
    # Преобразуем списки в numpy массивы для удобства использования
    velocity = np.array(velocity)
    return velocity[-1]

