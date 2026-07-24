"""Regression tests for CanvasOverlay._crop_draw_rect.

The crop-draw rect once used `p2 or p1` to pick the drag end point. QPointF is
falsy at the origin, so a drag ending exactly at the top-left corner (0, 0)
wrongly fell back to the start point and collapsed to a zero-size rect. The
helper now compares with `is not None`; these tests pin that behaviour.
"""

from PyQt6.QtCore import QPointF, QRectF

from negpy.desktop.view.canvas.overlay import CanvasOverlay


def _overlay_with_points(p1: QPointF | None, p2: QPointF | None) -> CanvasOverlay:
    # Bypass __init__ (a full QWidget/AppState) — the helper only reads the two
    # drag points and builds a QRectF (a pure QtCore value type).
    overlay = CanvasOverlay.__new__(CanvasOverlay)
    overlay._crop_draw_p1 = p1
    overlay._crop_draw_p2 = p2
    return overlay


def test_uses_p2_even_when_at_origin() -> None:
    # The bug: with `p2 or p1`, QPointF(0, 0) is falsy so `end` became p1,
    # yielding a zero-size rect at (120, 90) instead of the (0,0)->(120,90) span.
    overlay = _overlay_with_points(QPointF(120.0, 90.0), QPointF(0.0, 0.0))
    rect = overlay._crop_draw_rect()
    assert rect.left() == 0.0
    assert rect.top() == 0.0
    assert rect.width() == 120.0
    assert rect.height() == 90.0


def test_falls_back_to_p1_before_first_move() -> None:
    # p2 unset (None): a click with no drag collapses to p1.
    overlay = _overlay_with_points(QPointF(50.0, 40.0), None)
    rect = overlay._crop_draw_rect()
    assert rect.width() == 0.0
    assert rect.height() == 0.0
    assert rect.topLeft() == QPointF(50.0, 40.0)


def test_normalizes_reversed_drag() -> None:
    # Dragging up and to the left still yields a positive-size normalized rect.
    overlay = _overlay_with_points(QPointF(100.0, 100.0), QPointF(40.0, 30.0))
    rect = overlay._crop_draw_rect()
    assert rect == QRectF(40.0, 30.0, 60.0, 70.0)
