"""from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsTextItem, 
                             QMenu, QAction, QDialog, QFormLayout,  
                             QPushButton, QVBoxLayout, QLabel)
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QBrush, QFont

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, x, y, size, node, color):
        super().__init__(-size / 2, -size / 2, size, size)
        self.setPos(QPointF(x, y))
        self.setBrush(QBrush(color))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.node = node  # Store the Node object
        
        # Add text label
        self.text_item = QGraphicsTextItem(node.label, self)
        self.text_item.setPos(-size / 4, -size / 4)
        self.text_item.setFont(QFont("Arial", 10))
        self.setZValue(2)  # Ensure nodes are above edges

    def contextMenuEvent(self, event):
        context_menu = QMenu()
        
        # Add an action to show article properties
        properties_action = QAction("Show Properties", context_menu)
        properties_action.triggered.connect(self.show_properties)
        context_menu.addAction(properties_action)
        
        context_menu.exec_(event.screenPos())
    
    def show_properties(self):
        dialog = NodePropertiesDialog(self)
        dialog.exec_()  # Show the dialog modally


class NodePropertiesDialog(QDialog):
    def __init__(self, node_item, parent=None):
        super(NodePropertiesDialog, self).__init__(parent)
        self.node_item = node_item
        self.node = node_item.node  # Access the Node object via NodeItem
        self.setWindowTitle("Node Properties")

        # Create widgets to display node properties
        self.label_label = QLabel(self.node.label)
        self.position_x_label = QLabel(str(self.node.position[0]))
        self.position_y_label = QLabel(str(self.node.position[1]))
        self.links_label = QLabel(', '.join(link.label for link in self.node.links))

        # Set up the layout
        layout = QFormLayout()
        layout.addRow(QLabel("Label:"), self.label_label)
        layout.addRow(QLabel("Position X:"), self.position_x_label)
        layout.addRow(QLabel("Position Y:"), self.position_y_label)
        layout.addRow(QLabel("Links:"), self.links_label)

        # Add a close button
        buttons_layout = QVBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)  # Close the dialog
        buttons_layout.addWidget(close_button)

        layout.addRow(buttons_layout)
        self.setLayout(layout)"""

from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsTextItem, 
                             QMenu, QAction, QDialog, QFormLayout,  
                             QPushButton, QVBoxLayout, QLabel)
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QBrush, QFont

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, x, y, size, node_key, color, network_dict):
        super(NodeItem, self).__init__(-size / 2, -size / 2, size, size)
        self.setPos(QPointF(x, y))
        self.setBrush(QBrush(color))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.node_key = node_key  # Store the Node key
        self.network_dict = network_dict  # Store the network_dict
        
        # Add text label
        self.text_item = QGraphicsTextItem(node_key, self)  # Use node_key as label
        self.text_item.setPos(-size / 4, -size / 4)
        self.text_item.setFont(QFont("Arial", 10))
        self.setZValue(2)  # Ensure nodes are above edges

    def contextMenuEvent(self, event):
        context_menu = QMenu()
        
        # Add an action to show node properties
        properties_action = QAction("Show Properties", context_menu)
        properties_action.triggered.connect(self.show_properties)
        context_menu.addAction(properties_action)
        
        context_menu.exec_(event.screenPos())
    
    def show_properties(self):
        dialog = NodePropertiesDialog(self.node_key, self.network_dict, self)
        dialog.exec_()  # Show the dialog modally



class NodePropertiesDialog(QDialog):
    def __init__(self, node_key, network_dict, parent=None):
        super(NodePropertiesDialog, self).__init__(parent)
        self.node_key = node_key
        self.network_dict = network_dict  # Get the Node object from network_dict
        self.node = self.network_dict[self.node_key]  # Get the Node object
        self.setWindowTitle("Node Properties")

        # Create widgets to display node properties
        self.label_label = QLabel(self.node_key)  # Show the node_key as label
        self.position_x_label = QLabel(str(self.node.position[0]))
        self.position_y_label = QLabel(str(self.node.position[1]))
        self.links_label = QLabel(', '.join(self.node.links))  # Show links as keys

        # Set up the layout
        layout = QFormLayout()
        layout.addRow(QLabel("Label:"), self.label_label)
        layout.addRow(QLabel("Position X:"), self.position_x_label)
        layout.addRow(QLabel("Position Y:"), self.position_y_label)
        layout.addRow(QLabel("Links:"), self.links_label)

        # Add a close button
        buttons_layout = QVBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)  # Close the dialog
        buttons_layout.addWidget(close_button)

        layout.addRow(buttons_layout)
        self.setLayout(layout)
