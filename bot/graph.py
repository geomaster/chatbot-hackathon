import os
import sys
import json
from .node import Node
class Graph:
    def __init__(self):
        self.nodes = dict()
        graph_file_loc = 'bot/graph.json'
        with open(graph_file_loc, encoding='utf-8') as graph_file:
            raw_nodes = json.load(graph_file)['tree']
        for node in raw_nodes:
            self.nodes[node['id']] = Node(node)

    def __getitem__(self, state_id):
        if state_id in self.nodes:
            return self.nodes.get(state_id)
        else:
            raise AttributeError

    def is_consistent(self, node_to, wit_info):
        for entity, val_list in self.nodes[node_to].entities_needed.items():
            if not entity in wit_info:
                return False
            for val in val_list:
                if not val in wit_info[entity]:
                    return False
        for entity, val_list in self.nodes[node_to].entities_refused.items():
            if len(val_list) == 0:
                if entity in wit_info:
                    return False
            else:
                for val in val_list:
                    if entity in wit_info and val in wit_info[entity]:
                        return False
        return True

    def get_next(self, node_from, wit_info):
        valid_next_nodes = []
        if not self.nodes.get(node_from):
            # Unknown state
            return []

        for node_to in self.nodes[node_from].children:
            if self.is_consistent(node_to, wit_info):
                valid_next_nodes.append(node_to)
        return valid_next_nodes
