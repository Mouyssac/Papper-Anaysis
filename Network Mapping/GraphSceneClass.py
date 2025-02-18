import networkx as nx
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor
from matplotlib import cm
from NodeItemClass import NodeItem
from EdgeItemClass import EdgeItem


"""
class GraphScene(QGraphicsScene):
    def __init__(self, network_dict, parent=None):
        super(GraphScene, self).__init__(parent)
        self.network_dict = network_dict
        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = []
        self.create_graph()

    def create_graph(self):
        self.graph.clear()
        self.nodes.clear()
        self.edges.clear()
        self.clear()  # Clear existing items in the scene

        # Add nodes and edges to the NetworkX graph
        for node, connections in self.network_dict.items():
            self.graph.add_node(node)
            for connection in connections:
                self.graph.add_edge(node, connection)

        # Calculate node positions
        pos = nx.spring_layout(self.graph, seed=42, k=1, iterations=100)
        degrees = dict(self.graph.degree())
        max_degree = max(degrees.values())
        min_degree = min(degrees.values())
        clusters = self.get_clusters()
        cluster_colors = {i: QColor(*self.get_color_for_cluster(i)) for i in range(len(clusters))}

        for node, (x, y) in pos.items():
            x, y = x * 400 + 400, y * 400 + 300  # Adjust coordinates to center the graph
            degree = degrees[node]
            size = 20 + (degree - min_degree) * 30 / (max_degree - min_degree)
            cluster_id = self.get_cluster_id(node, clusters)
            color = cluster_colors[cluster_id]
            
            node_item = NodeItem(x, y, size, node, color)
            node_item.setData(0, node)
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

    def update_graph(self, network_dict):
        self.network_dict = network_dict
        self.create_graph()
"""
"""
class GraphScene(QGraphicsScene):
    def __init__(self, network_dict, parent=None):
        super(GraphScene, self).__init__(parent)
        self.network_dict = network_dict
        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = []
        self.create_graph()

    def create_graph(self):
        self.graph.clear()
        self.nodes.clear()
        self.edges.clear()
        self.clear()  # Clear existing items in the scene

        # Add nodes and edges to the NetworkX graph
        for node_label, node in self.network_dict.items():
            # Add node to the graph
            self.graph.add_node(node_label, position=node.position)
            print(f"Added node: {node_label} at position {node.position}")
            
            # Add edges to the graph
            for link in node.links:
                if link.label in self.network_dict:
                    self.graph.add_edge(node_label, link.label)
                    print(f"Added edge: {node_label} -> {link.label}")
                else:
                    print(f"Warning: Connection {link.label} not found in network_dict.")

        # Define size parameters
        min_size = 10
        max_size = 50

        # Determine the maximum degree
        max_degree = max(len(node.links) for node in self.network_dict.values())

        # Add nodes to the scene with specified positions
        for node_label, node in self.network_dict.items():
            x, y = node.position  # Use the position specified in the Node class
           
            degree = len(node.links)
            if max_degree > 0:
                size = min_size + (degree / max_degree) * (max_size - min_size)
            else:
                size = min_size
           
            color = QColor(100, 150, 200)  # Default color for nodes

            node_item = NodeItem(x, y, size, node, color)
            node_item.setData(0, node_label)
            self.nodes[node_label] = node_item
            self.addItem(node_item)

        # Add edges to the scene
        for start_node, end_node in self.graph.edges:
            if start_node in self.nodes and end_node in self.nodes:
                start_item = self.nodes[start_node]
                end_item = self.nodes[end_node]
                edge_item = EdgeItem(start_item, end_item)
                self.edges.append(edge_item)
                self.addItem(edge_item)
            else:
                print(f"Warning: Edge ({start_node}, {end_node}) references missing node(s).")

    def update_graph(self, network_dict):
        self.network_dict = network_dict
        self.create_graph()

    def mouseMoveEvent(self, event):
        super(GraphScene, self).mouseMoveEvent(event)
        for edge_item in self.edges:
            edge_item.update_position()
            """

class GraphScene(QGraphicsScene):
    def __init__(self, network_dict, parent=None):
        super(GraphScene, self).__init__(parent)
        self.network_dict = network_dict
        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = []
        self.create_graph()

    def create_graph(self):
        self.graph.clear()
        self.nodes.clear()
        self.edges.clear()
        self.clear()  # Clear existing items in the scene

        # Add nodes and edges to the NetworkX graph
        for node_key, node in self.network_dict.items():
            # Add node to the graph
            self.graph.add_node(node_key, position=node.position)
            print(f"Added node: {node_key} at position {node.position}")
            
            # Add edges to the graph
            for link_key in node.links:
                if link_key in self.network_dict:
                    self.graph.add_edge(node_key, link_key)
                    print(f"Added edge: {node_key} -> {link_key}")
                else:
                    print(f"Warning: Connection {link_key} not found in network_dict.")

        # Define size parameters
        min_size = 10
        max_size = 50

        # Determine the maximum degree
        max_degree = max(len(node.links) for node in self.network_dict.values())

        # Add nodes to the scene with specified positions
        for node_key, node in self.network_dict.items():
            x, y = node.position  # Use the position specified in the Node class
            
            # Calculate node size based on degree
            degree = len(node.links)
            size = min_size + (degree / max_degree) * (max_size - min_size) if max_degree > 0 else min_size
            
            color = QColor(100, 150, 200)  # Default color for nodes

            node_item = NodeItem(x, y, size, node_key, color)  # Pass node_key as label
            node_item.setData(0, node_key)
            self.nodes[node_key] = node_item
            self.addItem(node_item)

        # Add edges to the scene
        for start_node, end_node in self.graph.edges:
            if start_node in self.nodes and end_node in self.nodes:
                start_item = self.nodes[start_node]
                end_item = self.nodes[end_node]
                edge_item = EdgeItem(start_item, end_item)
                self.edges.append(edge_item)
                self.addItem(edge_item)
            else:
                print(f"Warning: Edge ({start_node}, {end_node}) references missing node(s).")

    def update_graph(self, network_dict):
        self.network_dict = network_dict
        self.create_graph()

    def mouseMoveEvent(self, event):
        super(GraphScene, self).mouseMoveEvent(event)
        for edge_item in self.edges:
            edge_item.update_position()