import numpy as np
import random

import matplotlib.pyplot as plt
import networkx as nx

# Classe Node
class Node:
    def __init__(self, label, position=(0.0, 0.0)):
        self.label = label
        self.position = (round(position[0], 2), round(position[1], 2))  # Position rounded to two decimals
        self.links = []

    def add_link(self, node):
        if node not in self.links:
            self.links.append(node)
    
    def add_link(self, node_key):
        if node_key not in self.links:
            self.links.append(node_key)
    
    def __repr__(self):
        return f"Node({self.label}, position={self.position}, links={self.links})"

# Gn rateur de r seau
def generate_network(num_clusters=5, nodes_per_cluster=4, num_influents=5):

    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon",
             "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", 
             "umbrella", "violet", "watermelon", "xylophone", "yogurt", "zebra", "ant", "butterfly", "cat",
             "dog", "elephant", "fox", "goat", "horse", "iguana", "jellyfish", "kangaroo", "lion", "monkey",
             "nightingale", "octopus", "penguin", "quail", "rabbit", "snake", "tiger", "urchin", "vulture",
             "whale", "xenops", "yak", "zebra", "airplane", "bicycle", "car", "drone", "elevator", "ferry",
             "glider", "helicopter", "icebreaker", "jet", "kayak", "locomotive", "motorcycle", "narrowboat",
             "oxcart", "parachute", "quadbike", "rocket", "submarine", "tractor", "unicycle", "van", "wagon",
             "xerox", "yacht", "zeppelin", "atom", "battery", "circuit", "diode", "electron", "fiber", "gauge",
             "hydrogen", "insulator", "joule", "kilowatt", "laser", "microchip", "neutron", "oscillator", 
             "photon", "quantum", "resistor", "sensor", "transistor", "ultrasound", "voltage", "watt"]


    network_dict = {}  # Dictionary to store nodes by their label
    node_id = 0
    nodes = []

    # Generate clusters
    for cluster_id in range(num_clusters):
        cluster_nodes = [Node(label=words[node_id + i], position=(random.uniform(-400, 400), random.uniform(-300, 300))) 
                         for i in range(nodes_per_cluster)]
        
        for index,node in enumerate(cluster_nodes):
            network_dict[f'Article_{index + node_id}'] = node
            nodes.append(node)

        node_id += nodes_per_cluster


        # Add dense connections within each cluster
        for i in range(len(cluster_nodes)):
            for j in range(i + 1, len(cluster_nodes)):
                if random.randint(1, 10) > 1:
                    key_i = f'Article_{node_id - len(cluster_nodes) + i}'
                    key_j = f'Article_{node_id - len(cluster_nodes) + j}'
                    node_i = network_dict[key_i]
                    node_j = network_dict[key_j]
                    node_i.add_link(key_j)
                    node_j.add_link(key_i)
    
    # Add connections between clusters
    for i in range(num_clusters):
        for j in range(i + 1, num_clusters):
            if random.randint(1, 10) > 6:
                # Find a random node from cluster i
                key_i = f'Article_{i * nodes_per_cluster + 1}'
                node_i = network_dict.get(key_i)
            
                # Find a random node from cluster j
                key_j = f'Article_{j * nodes_per_cluster + 1}'
                node_j = network_dict.get(key_j)
            
                if node_i and node_j:
                    # Add connection between the two nodes
                    node_i.add_link(key_j)
                    node_j.add_link(key_i)

    
    # Add influential nodes
    influents_keys = np.random.choice(list(network_dict.keys()), num_influents, replace=False)
    influents = [network_dict[key] for key in influents_keys]

    for influent in influents:
        other_keys = [key for key in network_dict if key != influent.label and len(network_dict[key].links) < 10]
        if other_keys:
            # Ensure we don't pick more nodes than available
            num_other_nodes = min(5, len(other_keys))
            other_keys_selected = np.random.choice(other_keys, num_other_nodes, replace=False)
            for other_key in other_keys_selected:
                other = network_dict[other_key]
                influent.add_link(other_key)
                other.add_link(influent.label)

    return network_dict



# Supposons que 'network_dict' est d j  cr   par votre g n rateur de r seau

def visualize_network(network_dict):
    G = nx.Graph()
    
    # Ajouter les n uds et les ar tes au graphe
    for key, node in network_dict.items():
        G.add_node(key, pos=node.position)
        for link_key in node.links:
            G.add_edge(key, link_key)
    
    # Extraire les positions des n uds
    pos = nx.spring_layout(G,k = 1, seed=42, iterations = 40)  # 'spring_layout' pour une disposition automatique
    labels = {key: key for key in network_dict.keys()}  #  tiquettes des n uds

    # Dessiner le r seau
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    plt.title('Network Visualization')
    plt.show()

# Exemple d'utilisation
# network_dict = generate_network()  # G n rer le r seau avec votre fonction
# visualize_network(network_dict)

network_dict = generate_network(num_clusters=5, nodes_per_cluster=4, num_influents=0)
visualize_network(network_dict)

