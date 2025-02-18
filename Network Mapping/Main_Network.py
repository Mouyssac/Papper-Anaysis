import sys
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QMessageBox, QAction, QPushButton, QVBoxLayout, QWidget
from GraphViewClass import GraphView
from PyQt5.QtWidgets import QInputDialog, QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
from GraphSceneClass import GraphScene
import json  # For saving and loading data
from Network_Generator import generate_network




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create and add a button to add nodes
        self.add_node_button = QPushButton("Add Node")
        self.add_node_button.clicked.connect(self.add_node)
        button_layout.addWidget(self.add_node_button)

        # Create and add a button to generate a graph
        self.generate_graph_button = QPushButton("Generate Graph")
        self.generate_graph_button.clicked.connect(self.generate_graph)
        button_layout.addWidget(self.generate_graph_button)

        # Organize with Louvain button
        self.organize_louvain_button = QPushButton("Organize with Louvain")
        self.organize_louvain_button.clicked.connect(self.organize_with_louvain)  # Assuming an organize_with_louvain method
        button_layout.addWidget(self.organize_louvain_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Create the scene and view
        self.network_dict = generate_network()
        #self.network_dict  = {'Article_1': [], 'Article_2': ['Article_3', 'Article_4', 'Article_28'], 'Article_3': ['Article_2', 'Article_24'], 'Article_4': ['Article_2', 'Article_13'], 'Article_5': ['Article_8', 'Article_15', 'Article_22'], 'Article_6': ['Article_13'], 'Article_7': [], 'Article_8': ['Article_5', 'Article_23', 'Article_22'], 'Article_9': ['Article_21', 'Article_24', 'Article_13'], 'Article_10': ['Article_11', 'Article_12', 'Article_21', 'Article_23', 'Article_24'], 'Article_11': ['Article_10', 'Article_12', 'Article_28', 'Article_13'], 'Article_12': ['Article_10', 'Article_11', 'Article_22'], 'Article_13': ['Article_21', 'Article_22', 'Article_4', 'Article_9', 'Article_11', 'Article_6', 'Article_16'], 'Article_14': ['Article_24'], 'Article_15': ['Article_5', 'Article_28'], 'Article_16': ['Article_23', 'Article_13'], 'Article_17': ['Article_18', 'Article_25'], 'Article_18': ['Article_17'], 'Article_19': [], 'Article_20': ['Article_23', 'Article_24'], 'Article_21': ['Article_10', 'Article_9', 'Article_13'], 'Article_22': ['Article_24', 'Article_12', 'Article_8', 'Article_23', 'Article_5', 'Article_13'], 'Article_23': ['Article_8', 'Article_20', 'Article_10', 'Article_16', 'Article_28', 'Article_22', 'Article_28'], 'Article_24': ['Article_22', 'Article_3', 'Article_10', 'Article_9', 'Article_20', 'Article_14', 'Article_28'], 'Article_25': ['Article_27', 'Article_17'], 'Article_26': ['Article_27'], 'Article_27': ['Article_25', 'Article_26'], 'Article_28': ['Article_23', 'Article_15', 'Article_2', 'Article_23', 'Article_24', 'Article_11']}
        self.scene = GraphScene(self.network_dict)
        self.view = GraphView(self.scene)
        main_layout.addWidget(self.view)

        self.setCentralWidget(central_widget)



  
  

    def add_node(self):
        print('function not implented yet')
        """
        # Input for new node details
        new_node_label, ok = QInputDialog.getText(self, "New Node", "Enter node label:")
        if not ok or not new_node_label:
            QMessageBox.warning(self, "Error", "Node label is required.")
            return

        # Input for node position
        new_node_position, ok = QInputDialog.getText(self, "Node Position", "Enter node position (x, y):")
        if not ok or not new_node_position:
            QMessageBox.warning(self, "Error", "Node position is required.")
            return

        try:
            x, y = map(float, new_node_position.split(','))
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid position format. Use 'x, y'.")
            return

        # Open dialog to select connections
        dialog = ConnectionDialog(self.network_dict.keys(), self)
        if dialog.exec_() == QDialog.Accepted:
            selected_nodes = dialog.get_selected_nodes()
            
            # Update network dictionary
            self.network_dict[new_node_label] = list(selected_nodes)
            for node in selected_nodes:
                self.network_dict[node].append(new_node_label)

            # Refresh the graph
            self.scene.update_graph(self.network_dict)"""

    def generate_graph(self):
        print('not implemented yet')

    def organize_with_louvain(self):
            print('not implemented yet')

class ConnectionDialog(QDialog):
    def __init__(self, nodes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Connections")
        self.setGeometry(100, 100, 300, 400)
        
        layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(nodes)
        layout.addWidget(QLabel("Select nodes to connect to:"))
        layout.addWidget(self.list_widget)
        
        button_box = QVBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_box.addWidget(self.ok_button)
        layout.addLayout(button_box)

    def get_selected_nodes(self):
        return set(item.text() for item in self.list_widget.selectedItems())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

