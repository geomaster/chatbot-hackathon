import os
import sys
import json
from .node import Node
from jsonschema import validate

class Graph:
    def __init__(self):
        self.nodes = dict()
        graph_file_loc = 'bot/graph.json'
        schema_file_loc = 'bot/schema.json'
        with open(graph_file_loc, encoding='utf-8') as graph_file:
            graph_json = json.load(graph_file)
        with open(schema_file_loc, encoding='utf-8') as schema_file:
            schema = json.load(schema_file)
        validate(graph_json, schema)
        for node in graph_json['tree']:
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
        for node_to in self.nodes[node_from].children:
            if self.is_consistent(node_to, wit_info):
                valid_next_nodes.append(node_to)
        return valid_next_nodes