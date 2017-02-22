class Node:
    def __init__(self, json_data):
        self.id = json_data['id']
        self.description = json_data['description']
        self.parent = json_data['parent']
        self.children = json_data['children']
        self.entities_needed = json_data['entities_needed']
        self.entities_refused = json_data['entities_refused']
        self.message = json_data['message']