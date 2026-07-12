# Path Forge
# Blender add-on for creating and editing paths
# Copyright (C) dmcoy
# Licensed under the GNU General Public License v3.0

from . import axis_reorientation
from . import ui

def register():
    axis_reorientation.register()
    ui.register()

def unregister():
    ui.unregister()
    axis_reorientation.unregister()

if __name__ == "__main__":
    register()