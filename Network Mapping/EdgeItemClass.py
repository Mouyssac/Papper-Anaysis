from PyQt5.QtWidgets import  QGraphicsLineItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

class EdgeItem(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.setPen(QPen(Qt.black))
        self.setZValue(1)  # Ensure edges are below nodes
        self.update_position()

    def update_position(self):
        start_pos = self.start_item.pos()
        end_pos = self.end_item.pos()
        self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
