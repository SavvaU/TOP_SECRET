import numpy as np
from scipy.stats import norm, multivariate_normal
import matplotlib.pyplot as plt
import plot_countour as cnt

def propability(spread, dist, contour):
    # Диапазон значений X и Y
    x_min, x_max = -spread * dist, spread * dist
    y_min, y_max = -spread * dist, spread * dist

    # Параметры нормальных распределений для X и Y (центрированные)
    mu_x, sigma_x = 0, x_max / 3  # Среднее и стандартное отклонение для X
    mu_y, sigma_y = 0, y_max / 3  # Среднее и стандартное отклонение для Y

    # Создаем сетку значений
    x = np.linspace(x_min, x_max, 200)
    y = np.linspace(y_min, y_max, 200)
    X, Y = np.meshgrid(x, y)

    # Вычисляем плотность вероятности
    Z = multivariate_normal.pdf(np.dstack((X, Y)), mean=[mu_x, mu_y], cov=[[sigma_x**2, 0], [0, sigma_y**2]])

    # Проверяем, какие точки находятся внутри контура
    from matplotlib.path import Path

    path = Path(contour)
    points = np.vstack((X.ravel(), Y.ravel())).T
    inside = path.contains_points(points)
    inside = inside.reshape(X.shape)

    # Интегрируем плотность вероятности внутри контура
    probability = np.sum(Z * inside) * (x[1] - x[0]) * (y[1] - y[0])
    return probability
#
#print(f"Вероятность попадания точки в контур: {probability}")
#
## Визуализация
#plt.contourf(X, Y, Z, levels=50, cmap='viridis')
#plt.plot(contour[:, 0], contour[:, 1], 'r-', linewidth=2)
#plt.scatter(X[inside], Y[inside], color='red', s=1)
#plt.colorbar(label='Плотность вероятности')
#plt.xlabel('X')
#plt.ylabel('Y')
#plt.title('Совместное нормальное распределение и контур')
#plt.text(0.05, 0.95, f'Вероятность: {probability:.4f}', ha='left', va='top', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
#plt.show()
