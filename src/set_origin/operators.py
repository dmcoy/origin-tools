"""Set origin operators for Blender objects.

Provides operators to set the origin of selected objects to various locations.
"""

import bpy


class OBJECT_OT_set_origin_to_geometry(bpy.types.Operator):
    """Set each selected object's origin to its geometry center."""
    bl_idname = "object.set_origin_to_geometry"
    bl_label = "Origin to geometry"
    bl_description = "Sets each selected object's origin to its geometry"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and context.selected_objects)

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")
        return {"FINISHED"}


class OBJECT_OT_set_geometry_to_origin(bpy.types.Operator):
    """Set each selected object's geometry to its origin."""
    bl_idname = "object.set_geometry_to_origin"
    bl_label = "Geometry to origin"
    bl_description = "Sets each selected object's geometry to the origin"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and context.selected_objects)

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN", center="MEDIAN")
        return {"FINISHED"}


class OBJECT_OT_set_origin_to_3d_cursor(bpy.types.Operator):
    """Set each selected object's origin to the 3D cursor position."""
    bl_idname = "object.set_origin_to_3d_cursor"
    bl_label = "Origin to 3D cursor"
    bl_description = "Sets each selected object's origin to the 3D cursor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and context.selected_objects)

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
        return {"FINISHED"}


class OBJECT_OT_set_origin_to_mass_surface(bpy.types.Operator):
    """Set each selected object's origin to its center of mass (surface)."""
    bl_idname = "object.set_origin_to_mass_surface"
    bl_label = "Origin to mass (surface)"
    bl_description = "Sets each selected object's origin to mass (surface)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and context.selected_objects)

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="MEDIAN")
        return {"FINISHED"}


class OBJECT_OT_set_origin_to_mass_volume(bpy.types.Operator):
    """Set each selected object's origin to its center of mass (volume)."""
    bl_idname = "object.set_origin_to_mass_volume"
    bl_label = "Origin to mass (volume)"
    bl_description = "Sets each selected object's origin to mass (volume)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and context.selected_objects)

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_VOLUME", center="MEDIAN")
        return {"FINISHED"}


class OBJECT_OT_set_origin_to_selection(bpy.types.Operator):
    """Set the origin to current selection (edit mode only).

    This operator requires being in edit mode and is primarily used for
    mesh objects. It sets the origin to the average position of all selected
    vertices. The 3D cursor is then snapped back to the world origin.
    """
    bl_idname = "object.set_origin_to_selection"
    bl_label = "Set origin to selection"
    bl_description = "Sets the origin to current selection (edit mode only)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(
            obj and obj.type == "MESH" and context.mode == "EDIT_MESH"
            and context.selected_objects
        )

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


# Operator classes
classes = [
    OBJECT_OT_set_origin_to_geometry,
    OBJECT_OT_set_geometry_to_origin,
    OBJECT_OT_set_origin_to_3d_cursor,
    OBJECT_OT_set_origin_to_mass_surface,
    OBJECT_OT_set_origin_to_mass_volume,
    OBJECT_OT_set_origin_to_selection,
]


def register():
    """Register all set origin operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all set origin operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)