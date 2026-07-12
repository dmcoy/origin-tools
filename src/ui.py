import bpy

class VIEW3D_PT_path_forge_panel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_path_forge_panel"
    bl_label = "Path Forge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Path Forge"
    
    def draw(self, context):
        axis_reorientation_properties = context.scene.axis_reorientation_properties
        layout = self.layout

        layout.label(text="Axis Reorientation", icon="EMPTY_AXIS")
        layout.row().prop(axis_reorientation_properties, "rotation_angle", text="Rotation Angle")

        row = layout.row(align=True)
        row.operator("object.rot_x_axis")
        row.operator("object.rot_y_axis")
        row.operator("object.rot_z_axis")

classes = [VIEW3D_PT_path_forge_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
