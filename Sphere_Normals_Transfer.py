# README! Script is experemental, so please, save all of files before running the script!
# 
# 1. Hide everything except the tree (if multiple objects, set <merged> variable to 0)
# 2. Select all of visible object and set any active
# 3. Run the script!
#
# Tree must have separated material for leaves!
# Tree must be only visible object in scene!
# Don't have to deselect object's mesh
# Don't have to set specific active object
# Tree may have other groups and modifiers

import bpy

def Sphere_Normals_Transfer():
    
    merged = 1  #if 1, will add Shrinkwrap modifier to sphere
    mat_num = 2  #number of materials
    leaves_num = 2  #leaves material number
    debug = 0  #if 1, will keep Sphere and NormalEdit modifiers
    
    #*** Snaping cursor and selecting leaves! ***

    bpy.context.area.ui_type = 'VIEW_3D'  #set active window

    # Set object and mesh
    active_obj = bpy.context.active_object 
    mesh = active_obj.data

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    # Select leaves material (first material)
    bpy.context.object.active_material_index = 1
    bpy.ops.object.material_slot_select()

    bpy.ops.view3d.snap_cursor_to_selected()  #cursor center of all leaves

    bpy.ops.object.mode_set(mode='OBJECT')

    #*** Creating sphere and transfering normals! ***
    
    # Set location and radius for sphere
    cursor_location = bpy.context.scene.cursor.location
    radius = max(active_obj.dimensions)
    
    # Create a sphere
    sph = bpy.ops.mesh.primitive_uv_sphere_add(radius = radius, location = cursor_location)
    bpy.ops.object.shade_smooth()
    bpy.context.object.name = "NSphere"
    
    if merged == 1:
        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        bpy.context.object.modifiers["Shrinkwrap"].target = active_obj
        bpy.context.object.modifiers["Shrinkwrap"].offset = radius/2
        if debug < 1:
            bpy.ops.object.modifier_apply(modifier="Shrinkwrap")

    # Select all objects except sphere
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.view_layer.objects:
        if obj.name != "NSphere":
            obj.select_set(True)

    # Group leaves and add modifier masked by leaves group
    for obj in bpy.context.selected_objects:
        if len(obj.material_slots) == mat_num:
            bpy.context.view_layer.objects.active = obj
            
            group = obj.vertex_groups.new(name="LeavesGroup")
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.vertex_group_assign()
            bpy.ops.object.mode_set(mode='OBJECT')
        
             #bpy.ops.object.modifier_add(type='NORMAL_EDIT')
             #bpy.context.object.modifiers["NormalEdit"].target = bpy.data.objects["NSphere"]
             #bpy.context.object.modifiers["NormalEdit"].vertex_group = "LeavesGroup"
            bpy.ops.object.modifier_add(type='DATA_TRANSFER')
            bpy.context.object.modifiers["DataTransfer"].object = bpy.data.objects["NSphere"]
            bpy.context.object.modifiers["DataTransfer"].vertex_group = "LeavesGroup"
            bpy.context.object.modifiers["DataTransfer"].use_loop_data = True
            bpy.context.object.modifiers["DataTransfer"].data_types_loops = {'CUSTOM_NORMAL'}

         
            if debug < 1:
                 #bpy.ops.object.modifier_apply(modifier="NormalEdit")
                bpy.ops.object.modifier_apply(modifier="DataTransfer")

    # Select sphere and delete it
    if debug < 1:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.view_layer.objects:
            if obj.name == "NSphere":
                obj.select_set(True)
        bpy.ops.object.delete(use_global=False)


    bpy.ops.view3d.snap_cursor_to_center()

    bpy.context.area.ui_type = 'TEXT_EDITOR'


def Duplicate_Objects_For_Transfer():
    
    bpy.ops.object.duplicate()
    
    for obj in bpy.context.selected_objects:
        nName = obj.name[:-4] + "_SphereNormals" #make new name
        obj.name = nName #assign new name
        
    bpy.context.area.ui_type = 'VIEW_3D'
    bpy.ops.object.hide_view_set(unselected=True) #hide original objects
    bpy.context.area.ui_type = 'TEXT_EDITOR'


# Calling functions
Duplicate_Objects_For_Transfer()
Sphere_Normals_Transfer()
