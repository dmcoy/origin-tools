import bpy

class VIEW3D_PT_origin_doctor_panel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_origin_doctor_panel"
    bl_label = "Origin Doctor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Origin Doctor"
    
    def draw(self, context):
        axis_reorientation_properties = context.scene.axis_reorientation_properties
        layout = self.layout

        # Axis Reorientation
        layout.label(text="Change Origin Orientation", icon="EMPTY_AXIS")
        layout.prop(axis_reorientation_properties, "rotation_angle", text="Rotation Angle")
        row = layout.row(align=True)
        row.operator("object.rot_x_axis")
        row.operator("object.rot_y_axis")
        row.operator("object.rot_z_axis")

        # Set origin one-click  
        layout.label(text="Set Origin (one-click)", icon="OBJECT_ORIGIN")
        layout.operator("object.set_origin_to_geometry")
        layout.operator("object.set_geometry_to_origin")
        layout.operator("object.set_origin_to_3d_cursor")
        layout.operator("object.set_origin_to_mass_surface")
        layout.operator("object.set_origin_to_mass_volume")
        layout.operator("object.set_origin_to_selection")


classes = [VIEW3D_PT_origin_doctor_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
