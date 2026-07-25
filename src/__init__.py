"""Origin Tools

Blender add-on for manipulating object origins
Copyright (C) 2026 dmcoy
Licensed under the GNU General Public License v3.0
"""

from . import orientation, align, set, ui


def register():
    orientation.register()
    align.register()
    set.register()
    ui.register()

def unregister():
    ui.unregister()
    set.unregister()
    align.unregister()
    orientation.unregister()

if __name__ == "__main__":
    register()