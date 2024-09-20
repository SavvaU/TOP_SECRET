import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import time


filename = 'Data/16810.stl'
# filename = 'Data/sphere.stl'

mesh_data = mesh.Mesh.from_file(filename)
vol, center_mass, Inertion = mesh_data.get_mass_properties()
print(center_mass)
mesh_data.rotate([0.0, 0.0, 0.5], np.deg2rad(30))  # Rotate mesh 90° on x axis

slicing_axis = 'Z'  # выбор оси
num_slices = 6  # количество слайсов

def slicing_mesh(mesh_data, slicing_axis, num_slices):
    """

    :param mesh_data:
    :param slicing_axis:
    :param num_slices:
    :return:
    """
    out_list = []
    if slicing_axis == 'X':
        num_axis = 0
    elif slicing_axis == 'Y':
        num_axis = 1
    elif slicing_axis == 'Z':
        num_axis = 2

    axis_range = mesh_data.points[:, num_axis]

    step_slising = int(len(axis_range) / num_slices)
    slice_positions = axis_range[0::step_slising]

    for i, slice_position in enumerate(slice_positions):
        # определение точности совпадения
        tolerance = 0.05
        mask = np.isclose(mesh_data.points[:, num_axis], slice_position, atol=tolerance)
        # Создание маски для среза
        if slicing_axis == 'X':
            sliced_vertices = np.vstack((mesh_data.points[mask][:, 1],
                                         mesh_data.points[mask][:, 2])).T
        elif slicing_axis == 'Y':
            sliced_vertices = np.vstack((mesh_data.points[mask][:, 0],
                                         mesh_data.points[mask][:, 2])).T
        elif slicing_axis == 'Z':
            # Извлечение вершин из слайсов
            sliced_vertices = mesh_data.points[mask][:, 0:2]
        hull = ConvexHull(sliced_vertices)
        out_list.append([sliced_vertices, hull])
    return out_list

if __name__=="__main__":
    slices_list = slicing_mesh(mesh_data, slicing_axis, num_slices)

    plt.figure()
    for sliced_vertices, hull in slices_list:
        print('площадь = {} м2'.format(hull.area))
        # Построение графиков
        time.sleep(0.5)
        plt.scatter(sliced_vertices[:, 0], sliced_vertices[:, 1], marker='*', s=1)
        plt.plot(np.hstack((sliced_vertices[hull.vertices, 0], sliced_vertices[hull.vertices[0], 0])),
                 np.hstack((sliced_vertices[hull.vertices, 1], sliced_vertices[hull.vertices[0], 1])), 'r-', lw=1)
        plt.axis('equal')
        plt.title(f'Slice')
        plt.xlabel('X')
        plt.ylabel('Y')
    plt.grid()
    plt.show()

    # my_mesh = mesh.Mesh.from_file('wheel.stl')
    # esh.vectors *= 5  # Scale mesh to 5 times bigger
    # mesh_data.rotate([0, 0.5, 0.0], np.deg2rad(90))  # Rotate mesh 90° on x axis
    # my_mesh.save('scaled_wheel.stl')
