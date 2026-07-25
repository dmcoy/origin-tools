"""Properties for orientation settings."""

import bpy


class orientation_properties(bpy.types.PropertyGroup):
    """Scene properties for controlling orientation behavior.

    Contains user-configurable parameters for the rotation angle applied
    when reorienting object local axes.
    """
    rotation_angle: bpy.props.FloatProperty(
        default=90.0,
        name="Rotation Angle",
        min=0.0,
        max=360.0,
        step=100,
        description="Angle in degrees"
    )


def register():
    """Register the orientation properties."""
    bpy.utils.register_class(orientation_properties)
    bpy.types.Scene.orientation_properties = (
        bpy.props.PointerProperty(type=orientation_properties)
    )


def unregister():
    """Unregister the orientation properties."""
    del bpy.types.Scene.orientation_properties
    bpy.utils.unregister_class(orientation_properties)