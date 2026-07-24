"""Small typing helpers for the PyQt6 view layer."""

from PyQt6.QtGui import QAction


def require_action(action: QAction | None) -> QAction:
    """Narrow a menu/toolbar ``addAction`` result to non-None.

    PyQt6 types ``QMenu.addAction`` / ``QWidget.addAction`` as returning
    ``QAction | None``, but for the overloads we use they always return a real
    QAction. This narrows the type at the call site without scattering asserts.
    """
    assert action is not None
    return action
