"""Orientation utilities.

Provides functions to rotate object local axes while preserving world orientation.
"""

import math
from mathutils import Matrix


def reorient_local_axes(context: dict, rotation_angle: float, axis: str) -> None:
    """Reorient the local axes of selected objects by a given rotation angle.

    Args:
        context: Blender context containing selected objects.
        rotation_angle: Angle in degrees to rotate around the specified axis.
        axis: Axis string ('X', 'Y', or 'Z') to rotate around.

    This rotates the local axes of all selected objects while preserving their
    world position and orientation. This can be useful for swapping origin axes
    (e.g., changing from Z-up to Y-up coordinate system).
    """
    # Create rotation matrix around the specified axis
    orientation = Matrix.Rotation(
        math.radians(rotation_angle), 4, axis
    )

    # Invert the orientation to apply to the mesh transform. This prevents
    # the mesh geometry from unintentional rotation when the axes are rotated.
    inverted_orientation = orientation.inverted()

    # Loop through selected objects and apply orientation
    for object in context.selected_objects:
        # Apply inverted orientation to the mesh data
        if hasattr(object, "data") and object.data is not None:
            object.data.transform(inverted_orientation)

        # Apply orientation to the local matrix
        object.matrix_local = object.matrix_local @ orientation