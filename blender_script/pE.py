import bpy

context = bpy.context


def Draw_Cone(vertices, r1, r2, l, h):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=l, location=(0, 0, h))
    cone = context.object
    #    bpy.context.object.rotation_euler[1] = 1.5708
    return cone


def Draw_Stage(vertices, r1, l, h):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r1, depth=l, location=(0, 0, h))
    cilinder = context.object
    #    bpy.context.object.rotation_euler[1] = 1.5708
    return cilinder


def draw_hitting_element_type_1(vertices, r, l1, l2):
    r1 = r
    r2 = 0
    # l1 =1
    # l2 =3
    h1 = 0  #
    h2 = -(l1 + l2) / 2
    cone_1 = Draw_Cone(vertices, r1, r2, l1, h1)
    cone_2 = Draw_Cone(vertices, r2, r1, l2, h2)


def draw_hitting_element_type_2(vertices, r, l1, l2):
    context = bpy.context
    r1 = r
    r2 = 0
    # l1 =1
    # l2 =3
    h1 = 0  #
    h2 = -(l1 + l2) / 2
    cone_1 = Draw_Cone(vertices, r1, r2, l1, h1)
    cilinder = Draw_Stage(vertices, r1, l2, h2)
    h3 = -(l2)
    cone_2 = Draw_Cone(vertices, r1, r2, l1, h3)

    mod = cilinder.modifiers.new("Boolean", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cone_2
    # large cube has context.
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
    context.scene.objects.unlink(cone_2)
    bpy.data.objects.remove(cone_2)


# Exporting into STL
def Save_to_STL(filepath):
    bpy.ops.object.select_all(action='SELECT')
    #    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.export_mesh.stl(check_existing=True, filepath="rocet_bpy.stl", filter_glob="*.stl", ascii=False,
                            use_mesh_modifiers=True, axis_forward='Y', axis_up='Z', global_scale=1.0)


# Main code

if __name__ == "__main__":
    r1 = 0.6
    l1 = 1
    l2 = 3

    vertices = 3

    draw_hitting_element_type_1(vertices, r1, l1, l2)
    # draw_hitting_element_type_2(vertices, r1, l1, l2)
    filepath = "hitting_element.stl"
    # bpy.ops.export_mesh.stl(filepath)
    Save_to_STL(filepath)
