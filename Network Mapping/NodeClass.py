class Node:
    def __init__(self, label, position=(0, 0)):
        self.label = label
        self.position = position  # Tuple (x, y)
        self.links = []

    def add_link(self, node):
        if node not in self.links:
            self.links.append(node)

    def __repr__(self):
        return f"Node({self.label}, position={self.position}, links={self.links})"
