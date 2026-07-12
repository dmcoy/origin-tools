import bpy

class axis_reorientation_properties(bpy.types.PropertyGroup):
    rotation_angle: bpy.props.FloatProperty(default=180.0, name="Rotation Angle", min=0.0, max=360.0, step=100.0, description="Angle in degrees")

def register():
    bpy.utils.register_class(axis_reorientation_properties)
    bpy.types.Scene.axis_reorientation_properties = bpy.props.PointerProperty(type=axis_reorientation_properties)
    
def unregister():
    del bpy.types.Scene.axis_reorientation_properties
    bpy.utils.unregister_class(axis_reorientation_properties)
