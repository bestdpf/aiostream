"""Gather the pipe operators."""

__all__ = []

from . import operator


def update_pipe_module():
    """Populate the pipe module dynamically."""
    module_dir = __all__
    operators = operator.__dict__
    for key, value in operators.items():
        if getattr(value, 'pipe', None):
            globals()[key] = value.pipe
            if key not in module_dir:
                module_dir.append(key)


# Populate the module
update_pipe_module()
