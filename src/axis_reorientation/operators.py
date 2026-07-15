import bpy
from . import utils

# Rotate X       
class OBJECT_OT_rot_x_axis_pos(bpy.types.Operator):
    bl_idname = "object.rot_x_axis_pos"
    bl_label = "+"
    bl_description = "Rotates the origin around the X axis (positive)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, arp.rotation_angle, "X")
        return {"FINISHED"}
    
class OBJECT_OT_rot_x_axis_neg(bpy.types.Operator):
    bl_idname = "object.rot_x_axis_neg"
    bl_label = "-"
    bl_description = "Rotates the origin around the X axis (negative)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, -arp.rotation_angle, "X")
        return {"FINISHED"}
    
# Rotate Y Pos
class OBJECT_OT_rot_y_axis_pos(bpy.types.Operator):
    bl_idname = "object.rot_y_axis_pos"
    bl_label = "+"
    bl_description = "Rotates the origin around the Y axis (positive)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, arp.rotation_angle, "Y")
        return {"FINISHED"}
    
# Rotate Y Neg
class OBJECT_OT_rot_y_axis_neg(bpy.types.Operator):
    bl_idname = "object.rot_y_axis_neg"
    bl_label = "-"
    bl_description = "Rotates the origin around the Y axis (negative)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, -arp.rotation_angle, "Y")
        return {"FINISHED"}
    
# Rotate Z  Pos
class OBJECT_OT_rot_z_axis_pos(bpy.types.Operator):
    bl_idname = "object.rot_z_axis_pos"
    bl_label = "+"
    bl_description = "Rotates the origin around the Z axis (positive)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, arp.rotation_angle, "Z")
        return {"FINISHED"}
    
# Rotate Z  Neg
class OBJECT_OT_rot_z_axis_neg(bpy.types.Operator):
    bl_idname = "object.rot_z_axis_neg"
    bl_label = "-"
    bl_description = "Rotates the origin around the Z axis (negative)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.selected_objects)
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, -arp.rotation_angle, "Z")
        return {"FINISHED"}

# Class to register
classes = [
    OBJECT_OT_rot_x_axis_pos,
    OBJECT_OT_rot_x_axis_neg,
    OBJECT_OT_rot_y_axis_pos,
    OBJECT_OT_rot_y_axis_neg,
    OBJECT_OT_rot_z_axis_pos,
    OBJECT_OT_rot_z_axis_neg,
]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)