import bpy
from . import utils

class OBJECT_OT_align_object_to_origin(bpy.types.Operator):
    bl_idname = ('object.align_object_to_origin')
    bl_label = 'Object to Origin'
    bl_description = 'Aligns object\'s mesh geometry to its current origin (experimental)'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == "MESH" and len(context.selected_objects) > 0)

    def execute(self, context):
        utils.align(context, utils.AlignMode.OBJECT_TO_ORIGIN)
        return {'FINISHED'}


class OBJECT_OT_align_origin_to_object(bpy.types.Operator):
    bl_idname = ('object.align_origin_to_object')
    bl_label = 'Origin to Object'
    bl_description = 'Aligns object\'s origin and orientation to mesh geometry (experimental)'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == "MESH" and len(context.selected_objects) > 0)

    def execute(self, context):
        utils.align(context, utils.AlignMode.ORIGIN_TO_OBJECT)
        return {'FINISHED'}


classes = [OBJECT_OT_align_object_to_origin, OBJECT_OT_align_origin_to_object]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)