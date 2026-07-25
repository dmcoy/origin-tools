"""Orientation module for manipulating object origins."""

from . import operators
from . import properties


def register():
    """Register all orientation operators and properties."""
    operators.register()
    properties.register()


def unregister():
    """Unregister all orientation operators and properties."""
    properties.unregister()
    operators.unregister()