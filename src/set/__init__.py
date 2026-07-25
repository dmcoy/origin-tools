"""Set origin module for Blender objects."""

from . import operators


def register():
    """Register all set operators."""
    operators.register()


def unregister():
    """Unregister all set operators."""
    operators.unregister()