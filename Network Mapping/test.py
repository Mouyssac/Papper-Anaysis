import sys
import numpy as np
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QMessageBox, QMenu, QAction
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush, QPen, QFont, QPainter, QColor
from matplotlib import cm

def generate_network_dict(num_clusters=5, nodes_per_cluster=10, num_influents=5):
    network_dict = {}
    node_id = 1

    # Generate clusters
    for cluster_id in range(num_clusters):
        cluster_nodes = [f"Article_{node_id + i}" for i in range(nodes_per_cluster)]
        node_id += nodes_per_cluster

        for node in cluster_nodes:
            network_dict[node] = []

        # Add dense connections within each cluster
        for i in range(len(cluster_nodes)):
            for j in range(i + 1, len(cluster_nodes)):
                network_dict[cluster_nodes[i]].append(cluster_nodes[j])
                network_dict[cluster_nodes[j]].append(cluster_nodes[i])

    # Add connections between clusters
    cluster_nodes = [node for node in network_dict.keys()]
    for i in range(num_clusters):
        for j in range(i + 1, num_clusters):
            node1 = np.random.choice([node for node in cluster_nodes if node.startswith(f"Article_{(i * nodes_per_cluster) + 1}")])
            node2 = np.random.choice([node for node in cluster_nodes if node.startswith(f"Article_{(j * nodes_per_cluster) + 1}")])
            network_dict[node1].append(node2)
            network_dict[node2].append(node1)

    # Add influential nodes
    influents = list(np.random.choice(cluster_nodes, num_influents, replace=False))
    for influent in influents:
        other_nodes = [node for node in cluster_nodes if node != influent and len(network_dict[node]) < 10]
        for other in np.random.choice(other_nodes, min(5, len(other_nodes)), replace=False):
            network_dict[influent].append(other)
            network_dict[other].append(influent)

    return network_dict

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, x, y, size, label, color):
        super().__init__(-size / 2, -size / 2, size, size)
        self.setPos(QPointF(x, y))
        self.setBrush(QBrush(color))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.label = label
        
        # Add text label
        self.text_item = QGraphicsTextItem(label, self)
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
        QMessageBox.information(None, "Article Properties", f"Article: {self.label}")

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

class GraphScene(QGraphicsScene):
    def __init__(self, network_dict, parent=None):
        super(GraphScene, self).__init__(parent)
        self.network_dict = network_dict
        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = []
        self.create_graph()

    def create_graph(self):
        # Add nodes and edges to the NetworkX graph
        for node, connections in self.network_dict.items():
            self.graph.add_node(node)
            for connection in connections:
                self.graph.add_edge(node, connection)

        # Calculate node positions
        pos = nx.spring_layout(self.graph, seed=42, k=0.5, iterations=100)

        # Calculate node sizes based on degree
        degrees = dict(self.graph.degree())
        max_degree = max(degrees.values())
        min_degree = min(degrees.values())

        # Calculate colors for clusters
        clusters = self.get_clusters()
        cluster_colors = {i: QColor(*self.get_color_for_cluster(i)) for i in range(len(clusters))}

        for node, (x, y) in pos.items():
            x, y = x * 400 + 400, y * 400 + 300  # Adjust coordinates to center the graph
            degree = degrees[node]
            size = 20 + (degree - min_degree) * 30 / (max_degree - min_degree)  # Size proportional to degree

            # Find the cluster to which the node belongs
            cluster_id = self.get_cluster_id(node, clusters)
            color = cluster_colors[cluster_id]
            
            node_item = NodeItem(x, y, size, node, color)
            node_item.setData(0, node)  # Add data to node
            self.nodes[node] = node_item
            self.addItem(node_item)

        for start_node, end_node in self.graph.edges:
            start_item = self.nodes[start_node]
            end_item = self.nodes[end_node]
            edge_item = EdgeItem(start_item, end_item)
            self.edges.append(edge_item)
            self.addItem(edge_item)

    def get_clusters(self):
        from networkx.algorithms.community import louvain_communities
        communities = louvain_communities(self.graph)
        clusters = [list(community) for community in communities]
        return clusters

    def get_cluster_id(self, node, clusters):
        for i, cluster in enumerate(clusters):
            if node in cluster:
                return i
        return -1

    def get_color_for_cluster(self, cluster_id):
        num_clusters = len(self.get_clusters())
        cmap = cm.get_cmap('Spectral', num_clusters)
        color = cmap(cluster_id)
        return tuple(int(c * 255) for c in color[:3])  # Convert RGBA to RGB

    def mouseMoveEvent(self, event):
        super(GraphScene, self).mouseMoveEvent(event)
        for edge_item in self.edges:
            edge_item.update_position()

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Viewer")
        self.setGeometry(100, 100, 800, 600)

        network_dict = generate_network_dict()
        self.scene = GraphScene(network_dict)
        self.view = GraphView(self.scene)

        self.setCentralWidget(self.view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
