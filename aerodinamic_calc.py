import numpy as np
from pandas import read_excel
import json

aero_data_6 = read_excel('Data\\Aerodinamik_data_.xlsx', sheet_name='Sixangle_T', index_col=0)
aero_data_4 = read_excel('Data\\Aerodinamik_data_.xlsx', sheet_name='Qadrant_T', index_col=0)
aero_data_3 = read_excel('Data\\Aerodinamik_data_.xlsx', sheet_name='Triangle_T', index_col=0)


# aero_data_3_dict = aero_data_3.to_dict()


def get_aero_koef(type_many_angle, alpha, h1, h2, r):
    """
    Получение аэродинамиечских коэффицентов
    :param type_many_angle:
    :param alpha:
    :param h1:
    :param h2:
    :param r:
    :return:
    """
    if type_many_angle == 'Tri':
        aero_dict = aero_data_3.to_dict()
    elif type_many_angle == 'Qudro':
        aero_dict = aero_data_4.to_dict()
    elif type_many_angle == 'Six':
        aero_dict = aero_data_6.to_dict()
    else:
        print('Указанный тип не соответствует: Tri, Qudro, Six')
        return

    Cx = None
    for k, v in enumerate(aero_dict):
        if type(v) == str:
            v_list = v.split('.')
            v_k = int(v_list[0])
        else:
            v_k = v

        if v_k == alpha:
            if aero_dict[v]['h1'] == h1 and aero_dict[v]['h2'] == h2 and aero_dict[v]['r'] == r:
                Cx = aero_dict[v]['Cx']
    return Cx


def make_table(type_many_angle, alpha, r):
    """
    Получение таблиц аэродинамических коэффицентов
    :param type_many_angle:
    :param alpha:
    :param r:
    :return:
    """
    array_cx = []

    list_koef = [0.01, 0.05, 0.1, 0.2, 0.3]

    for h1 in list_koef:
        list_cx = []
        for h2 in list_koef:
            list_cx.append(get_aero_koef(type_many_angle, alpha, h1, h2, r))
        array_cx.append(list_cx)

    return np.array(array_cx)


def neigborn_nan(array_koef, list_koef):
    """
    Функция для определения количества не пустых элементов массива по трем осям
    :param array_koef: массив размерностью nх3
    :param list_koef: индекс элемента массива для контроля
    :return:
    """
    i, j, k = list_koef
    weight_neigborn = [0, 0, 0]
    if np.isnan(array_koef[i, j, k]):
        ## i
        if i + 1 >= array_koef.shape[0]:
            weight_neigborn[0] += 0
        else:
            if np.isnan(array_koef[i + 1, j, k]):
                weight_neigborn[0] += 0
            else:
                 weight_neigborn[0] += 1

            if np.isnan(array_koef[i - 1, j, k]) or i - 1 < 0:
                weight_neigborn[0] += 0
            else:
                weight_neigborn[0] += 1
        ## j
        if j + 1 >= array_koef.shape[1]:
            weight_neigborn[1] += 0
        else:
            if np.isnan(array_koef[i, j + 1, k]):
                weight_neigborn[1] += 0
            else:
                weight_neigborn[1] += 1

            if np.isnan(array_koef[i, j - 1, k]) or j - 1 < 0:
                weight_neigborn[1] += 0
            else:
                weight_neigborn[1] += 1
        ## k
        if k + 1 >= array_koef.shape[2]:
            weight_neigborn[2] += 0
        else:
            if np.isnan(array_koef[i, j, k + 1]):
                weight_neigborn[2] += 0
            else:
                weight_neigborn[2] += 1

            if np.isnan(array_koef[i, j, k - 1]) or k - 1 < 0:
                weight_neigborn[2] += 0
            else:
                weight_neigborn[2] += 1

    else:
        weight_neigborn = [0, 0, 0]

    return weight_neigborn


def neigborn_nan_array(array_koef):
    """
    Функция для определения наличия не пустых элементов массива по всем осям
    :param array_koef:
    :return:
    """
    neigborn_array = []
    i_max, j_max, k_max = array_koef.shape
    for i in range(i_max):
        neigborn_array_j = []
        for j in range(j_max):
            neigborn_array_k = []
            for k in range(k_max):
                neigborn_array_k.append(neigborn_nan(array_koef, [i, j, k]))
            neigborn_array_j.append(neigborn_array_k)
        neigborn_array.append(neigborn_array_j)

    neigborn_array = np.array(neigborn_array)

    return neigborn_array


if __name__ == '__main__':
    type_many_angle = 'Tri'
    type_many_angle = 'Six'

    type_many_angle = 'Qudro'

    alpha = 0
    h_1 = 0.1
    h_2 = 0.1
    r = 0.05

    Cx_cur = get_aero_koef(type_many_angle, alpha, h_1, h_2, r)

    print('Значение C_x = {}'.format(Cx_cur))
    # 3-d массив аэродинамического коэффциента Cx
    c_x_3_d = []
    for i in [0.01, 0.05, 0.1, 0.2, 0.3]:
        c_x_3_d.append(make_table('Qudro', 0, i))
    c_x_3_d = np.array(c_x_3_d)

    print('вес c_x_3_d = {}'.format(neigborn_nan(c_x_3_d, [1, 2, 0])))

    c_x_3_d_neigborn_arr = neigborn_nan_array(c_x_3_d)
    c_x_3_d_neigborn = np.sum(c_x_3_d_neigborn_arr, axis=3)
    # индекс максимального элемента

