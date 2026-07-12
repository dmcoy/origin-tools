import math
from mathutils import Matrix

def reorient_local_axes(context, rotation_angle, axis):
    # create rotation matrix around the specified axis
    axis_reorientation = Matrix.Rotation(math.radians(rotation_angle), 4, axis)
    # also invert the reorientation to apply to the mesh transform
    # this prevents the mesh from unintentional rotation
    inverted_axis_reorientation = axis_reorientation.inverted() # try inverted safe???
    # loop through selected objects and apply axis reorientation
    for object in context.selected_objects:
        # apply inverted reorientation
        object.data.transform(inverted_axis_reorientation)
        # apply axis reorientation
        object.matrix_local = object.matrix_local @ axis_reorientation