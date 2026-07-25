"""Set origin module."""

from . import operators


def register():
    """Register all set origin operators."""
    operators.register()


def unregister():
    """Unregister all set origin operators."""
    operators.unregister()