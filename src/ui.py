import bpy

class VIEW3D_PT_origin_tools_panel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_origin_tools_panel"
    bl_label = "Origin"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    
    def draw(self, context):
        axis_reorientation_properties = context.scene.axis_reorientation_properties
        layout = self.layout

        # Axis Reorientation
        layout.label(text="Orientation:")#, icon="EMPTY_AXIS")
        layout.prop(axis_reorientation_properties, "rotation_angle", text="Rotation Angle")

        # Axis Reorientation labels
        row = layout.row()
        sub = row.row()
        sub.alignment = "CENTER"
        sub.label(text="X")
        sub = row.row()
        sub.alignment = "CENTER"
        sub.label(text="Y")
        sub = row.row()
        sub.alignment = "CENTER"
        sub.label(text="Z")

        # Axis Reorientation operators
        row = layout.row()
        column = row.column(align=True)
        column.operator("object.rot_x_axis_pos")
        column.operator("object.rot_x_axis_neg")
        column = row.column(align=True)
        column.operator("object.rot_y_axis_pos")
        column.operator("object.rot_y_axis_neg")
        column = row.column(align=True)
        column.operator("object.rot_z_axis_pos")
        column.operator("object.rot_z_axis_neg")

        # Set origin operators
        layout.label(text="Set Origin:")#, icon="OBJECT_ORIGIN")
        column = layout.column(align=True)
        column.operator("object.set_origin_to_geometry")
        column.operator("object.set_geometry_to_origin")
        column.operator("object.set_origin_to_3d_cursor")
        column.operator("object.set_origin_to_mass_surface")
        column.operator("object.set_origin_to_mass_volume")
        layout.operator("object.set_origin_to_selection")


classes = [VIEW3D_PT_origin_tools_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
