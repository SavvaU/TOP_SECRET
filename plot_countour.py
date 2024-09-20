import matplotlib.pyplot as plt
import numpy as np

cont = np.loadtxt('contour.txt', delimiter=',')
cont[:, 1] = np.max(cont[:, 1]) - cont[:, 1]

cont[:, 1] = cont[:, 1] - int(np.max(cont[:, 1]) / 2)
cont[:, 0] = cont[:, 0] - int(np.max(cont[:, 0]) / 2)

# ширина в метрах
l_m = 0.35
# ширина в пикселях
l_pix = np.max(cont[:, 0]) - np.min(cont[:, 0])

k_l = l_m / l_pix  # коэффицинент масштаба по длине

# высота в метрах
h_m = 0.25
# высота в пикселях
h_pix = np.max(cont[:, 1]) - np.min(cont[:, 1])

k_h = h_m / h_pix  # коэффицинент масштаба по


def in_contour(cnt_x, cnt_y, x, y):
    """
    Функция для нахождения лежит ли точка в контуре
    :param cnt_x: координты x контура
    :param cnt_y: координты y контура
    :param x: координты x точки
    :param y: координты y точки
    :return:
    """
    c = 0
    for i in range(len(cnt_x)):
        if (((cnt_y[i] <= y and y < cnt_y[i - 1]) or (cnt_y[i - 1] <= y
                                                      and y < cnt_y[i]))
                and (x > (cnt_x[i - 1] - cnt_x[i]) * (y - cnt_y[i]) /
                     (cnt_y[i - 1] - cnt_y[i]) + cnt_x[i])):
            c = 1 - c
    return bool(c)


if __name__ == '__main__':
    print('ширина в пикселях:', np.max(cont[:, 0]) - np.min(cont[:, 0]))
    print('высота в пикселях:', np.max(cont[:, 1]) - np.min(cont[:, 1]))
    # plt.plot(cont[:, 0], cont[:, 1])
    plt.plot(cont[:, 0], cont[:, 1])
    plt.grid()
    plt.show()
