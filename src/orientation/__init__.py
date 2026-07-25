"""Orientation module."""

from . import operators
from . import properties


def register():
    """Register all axis orientation operators and properties."""
    operators.register()
    properties.register()


def unregister():
    """Unregister all axis orientation operators and properties."""
    properties.unregister()
    operators.unregister()