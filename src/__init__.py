# Origin Tools
# Blender add-on for manipulating object origins
# Copyright (C) dmcoy
# Licensed under the GNU General Public License v3.0

from . import axis_reorientation, repair, set_origin, ui

def register():
    axis_reorientation.register()
    repair.register()
    set_origin.register()
    ui.register()

def unregister():
    ui.unregister()
    set_origin.unregister()
    repair.unregister()
    axis_reorientation.unregister()

if __name__ == "__main__":
    register()