import bpy

# Set origin to geometry
class OBJECT_OT_set_origin_to_geometry(bpy.types.Operator):
    bl_idname = "object.set_origin_to_geometry"
    bl_label = "Origin to geometry"
    bl_description = "Sets each selected object's origin to its geometry"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)

    def execute(self, context):
        for object in context.selected_objects:
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        return {"FINISHED"}

# Set geometry to origin
class OBJECT_OT_set_geometry_to_origin(bpy.types.Operator):
    bl_idname = "object.set_geometry_to_origin"
    bl_label = "Geometry to origin"
    bl_description = "Sets each selected object's geometry to the origin"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)

    def execute(self, context):
        for object in context.selected_objects:
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        return {"FINISHED"}

# Set origin to 3D cursor
class OBJECT_OT_set_origin_to_3d_cursor(bpy.types.Operator):
    bl_idname = "object.set_origin_to_3d_cursor"
    bl_label = "Origin to 3D cursor"
    bl_description = "Sets each selected object's origin to the 3D cursor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)

    def execute(self, context):
        for object in context.selected_objects:
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {"FINISHED"}
    
# Set origin to mass (surface)
class OBJECT_OT_set_origin_to_mass_surface(bpy.types.Operator):
    bl_idname = "object.set_origin_to_mass_surface"
    bl_label = "Origin to mass (surface)"
    bl_description = "Sets each selected object's origin to mass (surface)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)

    def execute(self, context):
        for object in context.selected_objects:
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        return {"FINISHED"}
    
# Set origin to mass (volume)
class OBJECT_OT_set_origin_to_mass_volume(bpy.types.Operator):
    bl_idname = "object.set_origin_to_mass_volume"
    bl_label = "Origin to mass (volume)"
    bl_description = "Sets each selected object's origin to mass (volume)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)

    def execute(self, context):
        for object in context.selected_objects:
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
        return {"FINISHED"}

# Set origin to selection  
class OBJECT_OT_set_origin_to_selection(bpy.types.Operator):
    bl_idname = "object.set_origin_to_selection"
    bl_label = "Set origin to selection"
    bl_description = "Sets the origin to current selection (edit mode only)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == "MESH" and context.mode == "EDIT_MESH" and context.selected_objects)

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        if context.mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
        if context.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")
        # Return cursor to world origin
        bpy.ops.view3d.snap_cursor_to_center()
        return {"FINISHED"}
    
classes = [
    OBJECT_OT_set_origin_to_geometry,
    OBJECT_OT_set_geometry_to_origin,
    OBJECT_OT_set_origin_to_mass_surface,
    OBJECT_OT_set_origin_to_mass_volume,
    OBJECT_OT_set_origin_to_3d_cursor,
    OBJECT_OT_set_origin_to_selection,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)