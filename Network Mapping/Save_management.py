import json

def save_workspace(network_dict, node_positions, filename='workspace.json'):
    with open(filename, 'w') as file:
        data = {
            'network': network_dict,
            'positions': node_positions
        }
        json.dump(data, file)

def load_workspace(filename='workspace.json'):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['network'], data['positions']
