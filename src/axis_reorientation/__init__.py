"""Axis reorientation module."""

from . import operators
from . import properties


def register():
    """Register all axis reorientation operators and properties."""
    operators.register()
    properties.register()


def unregister():
    """Unregister all axis reorientation operators and properties."""
    properties.unregister()
    operators.unregister()