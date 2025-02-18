
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter

class GraphView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(GraphView, self).__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.ctrl_pressed = False
        self.middle_button_pressed = False
        self.last_mouse_position = QPointF()  # Track the last mouse position

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = True
        super(GraphView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False
        super(GraphView, self).keyReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_button_pressed = True
            self.setCursor(Qt.ClosedHandCursor)
            self.last_mouse_position = event.pos()  # Store the initial mouse position
        super(GraphView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_button_pressed = False
            self.setCursor(Qt.ArrowCursor)
        super(GraphView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.middle_button_pressed:
            # Calculate the difference in position
            delta = event.pos() - self.last_mouse_position
            self.last_mouse_position = event.pos()  # Update the last position

            # Scroll the view by the delta amount
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        elif self.ctrl_pressed and event.buttons() & Qt.LeftButton:
            # Pan the view while holding Ctrl and left mouse button
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            super(GraphView, self).mouseMoveEvent(event)
        else:
            # Handle node dragging
            self.setDragMode(QGraphicsView.RubberBandDrag)
            super(GraphView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        if self.ctrl_pressed:
            # Zoom in and out with Ctrl and mouse wheel
            factor = 1.2
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor
            self.scale(factor, factor)
        else:
            super(GraphView, self).wheelEvent(event)
