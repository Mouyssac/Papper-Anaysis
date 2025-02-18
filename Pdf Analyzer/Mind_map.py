import tkinter as tk
import random
import math
from collections import defaultdict

class SimpleMindMap:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Mind Map")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.nodes = []
        self.links = []
        self.node_sizes = {}
        self.adjacency_matrix = []

        self.colors = ["#ffb3ba", "#ffdfba", "#ffffba", "#baffc9", "#bae1ff"]

        self.create_cluster(400, 300, 30)

        self.selected_node = None
        self.offset_x = 0
        self.offset_y = 0

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Organize", command=self.organize)

    def create_node(self, x, y, r, color):
        node = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black", width=2)
        self.nodes.append(node)
        self.node_sizes[node] = r
        return node

    def create_link(self, node1, node2):
        x1, y1, x2, y2 = self.canvas.coords(node1)
        cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2
        x1, y1, x2, y2 = self.canvas.coords(node2)
        cx2, cy2 = (x1 + x2) / 2, (y1 + y2) / 2
        link = self.canvas.create_line(cx1, cy1, cx2, cy2, fill="gray", width=2)
        self.links.append((link, node1, node2))

        index1 = self.nodes.index(node1)
        index2 = self.nodes.index(node2)
        self.adjacency_matrix[index1][index2] = 1
        self.adjacency_matrix[index2][index1] = 1

    def create_cluster(self, center_x, center_y, num_nodes):
        self.adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]

        cluster_color = random.choice(self.colors)
        
        for i in range(num_nodes):
            r = random.randint(20, 50)
            x = random.randint(r, 800 - r)
            y = random.randint(r, 600 - r)
            node = self.create_node(x, y, r, cluster_color)

        for _ in range(num_nodes - 1):
            n1, n2 = random.sample(self.nodes[-num_nodes:], 2)
            self.create_link(n1, n2)
            self.update_node_size(n1)
            self.update_node_size(n2)

    def update_node_size(self, node):
        self.node_sizes[node] += 5
        x1, y1, x2, y2 = self.canvas.coords(node)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        r = self.node_sizes[node]
        self.canvas.coords(node, cx-r, cy-r, cx+r, cy+r)

    def on_click(self, event):
        for node in self.nodes:
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 < event.x < x2 and y1 < event.y < y2:
                self.selected_node = node
                self.offset_x = event.x - (x1 + x2) / 2
                self.offset_y = event.y - (y1 + y2) / 2
                break

    def on_drag(self, event):
        if self.selected_node:
            x1, y1, x2, y2 = self.canvas.coords(self.selected_node)
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = event.x - cx, event.y - cy
            self.canvas.move(self.selected_node, dx, dy)
            self.update_links()

    def on_release(self, event):
        self.selected_node = None

    def update_links(self):
        for link, node1, node2 in self.links:
            x1, y1, x2, y2 = self.canvas.coords(node1)
            cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2
            x1, y1, x2, y2 = self.canvas.coords(node2)
            cx2, cy2 = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.coords(link, cx1, cy1, cx2, cy2)

    def on_mouse_move(self, event):
        for node in self.nodes:
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 < event.x < x2 and y1 < event.y < y2:
                self.canvas.itemconfig(node, outline="yellow")
            else:
                self.canvas.itemconfig(node, outline="black")

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def organize(self):
        sorted_nodes = sorted(self.nodes, key=lambda node: self.node_sizes[node], reverse=True)
        
        center_x, center_y = 400, 300
        max_radius = 200

        for i, node in enumerate(sorted_nodes):
            r = self.node_sizes[node]
            angle = 2 * math.pi * i / len(sorted_nodes)
            dist = max_radius * (1 - i / len(sorted_nodes))
            x = center_x + dist * math.cos(angle)
            y = center_y + dist * math.sin(angle)
            self.canvas.coords(node, x-r, y-r, x+r, y+r)

        for _ in range(10):
            self.reposition_nodes()

        self.update_links()

    def reposition_nodes(self):
        clusters = self.detect_clusters()
        for cluster in clusters:
            self.optimize_cluster_position(cluster)

    def detect_clusters(self):
        visited = set()
        clusters = []

        for i in range(len(self.nodes)):
            if i not in visited:
                cluster = self.bfs(i, visited)
                clusters.append(cluster)

        return clusters

    def bfs(self, start_node_index, visited):
        cluster = []
        queue = [start_node_index]
        visited.add(start_node_index)

        while queue:
            node_index = queue.pop(0)
            cluster.append(node_index)

            for neighbor_index, connected in enumerate(self.adjacency_matrix[node_index]):
                if connected and neighbor_index not in visited:
                    queue.append(neighbor_index)
                    visited.add(neighbor_index)

        return cluster

    def optimize_cluster_position(self, cluster):
        center_x, center_y = 400, 300

        for _ in range(10):
            for node_index in cluster:
                node = self.nodes[node_index]
                x1, y1, x2, y2 = self.canvas.coords(node)
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = 0, 0

                for other_index in cluster:
                    if node_index == other_index:
                        continue
                    other_node = self.nodes[other_index]
                    ox1, oy1, ox2, oy2 = self.canvas.coords(other_node)
                    ocx, ocy = (ox1 + ox2) / 2, (oy1 + oy2) / 2
                    distance = math.sqrt((cx - ocx) ** 2 + (cy - ocy) ** 2)
                    min_dist = (self.node_sizes[node] + self.node_sizes[other_node]) * 1.2

                    if distance < min_dist:
                        angle = math.atan2(cy - ocy, cx - ocx)
                        dx += (min_dist - distance) * math.cos(angle)
                        dy += (min_dist - distance) * math.sin(angle)

                self.canvas.move(node, dx, dy)

            self.separate_clusters(cluster, center_x, center_y)

    def separate_clusters(self, cluster, center_x, center_y):
        for node_index in cluster:
            node = self.nodes[node_index]
            x1, y1, x2, y2 = self.canvas.coords(node)
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

            dist_to_center = math.sqrt((cx - center_x) ** 2 + (cy - center_y) ** 2)
            if dist_to_center > 250:
                angle = math.atan2(cy - center_y, cx - center_x)
                self.canvas.move(node, -50 * math.cos(angle), -50 * math.sin(angle))

# Creer la fenetre principale Tkinter
root = tk.Tk()
app = SimpleMindMap(root)
root.mainloop()
