import bpy
from . import utils

# Rotate X       
class OBJECT_OT_rot_x_axis(bpy.types.Operator):
    bl_idname = "object.rot_x_axis"
    bl_label = "X"
    bl_description = "Changes orientation of the X axis"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, arp.rotation_angle, "Y")
        return {"FINISHED"}
    
# Rotate Y       
class OBJECT_OT_rot_y_axis(bpy.types.Operator):
    bl_idname = "object.rot_y_axis"
    bl_label = "Y"
    bl_description = "Changes orientation of the Y axis"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, arp.rotation_angle, "Z")
        return {"FINISHED"}
    
# Rotate Z  
class OBJECT_OT_rot_z_axis(bpy.types.Operator):
    bl_idname = "object.rot_z_axis"
    bl_label = "Z"
    bl_description = "Changes orientation of the Z axis"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        arp = context.scene.axis_reorientation_properties
        utils.reorient_local_axes(context, arp.rotation_angle, "X")
        return {"FINISHED"}

# Class to register
classes = [
    OBJECT_OT_rot_x_axis,
    OBJECT_OT_rot_y_axis,
    OBJECT_OT_rot_z_axis,
]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)