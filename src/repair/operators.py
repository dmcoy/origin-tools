"""Align module - mesh alignment utilities."""

import bpy
from . import utils


class OBJECT_OT_align_object_to_origin(bpy.types.Operator):
    """Align object mesh to its current origin.

    Aligns the selected mesh object's geometry to match its current origin
    and orientation. Useful for correcting meshes that were created or imported
    with incorrect axis orientation.

    Experimental - behavior may vary depending on mesh complexity.
    """
    bl_idname = "object.align_object_to_origin"
    bl_label = "Object to Origin"
    bl_description = "Aligns object's mesh geometry to its current origin (experimental)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and obj.type == "MESH" and context.selected_objects)

    def execute(self, context):
        utils.align(context, utils.AlignMode.OBJECT_TO_ORIGIN)
        return {"FINISHED"}


class OBJECT_OT_align_origin_to_object(bpy.types.Operator):
    """Align object origin to its mesh geometry.

    Aligns the selected mesh object's origin and orientation to match the
    dominant axis of the mesh geometry. Uses RANSAC algorithm for robust
    alignment.

    Experimental - behavior may vary depending on mesh complexity.
    """
    bl_idname = "object.align_origin_to_object"
    bl_label = "Origin to Object"
    bl_description = "Aligns object's origin and orientation to mesh geometry (experimental)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and obj.type == "MESH" and context.selected_objects)

    def execute(self, context):
        utils.align(context, utils.AlignMode.ORIGIN_TO_OBJECT)
        return {"FINISHED"}


# Operator classes
classes = [
    OBJECT_OT_align_object_to_origin,
    OBJECT_OT_align_origin_to_object,
]


def register():
    """Register all repair operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all repair operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)