import os
import sys
import json
from .node import Node

class Graph:
    def __init__(self):
        self.nodes = dict()
        self.starting_state = 'GREETING'
        fileloc = 'bot/graph.json' # TODO: this is ugly
        with open(fileloc) as graph_file:    
            raw_nodes = json.load(graph_file, encoding='utf-8')['tree']
        for node in raw_nodes:
            self.nodes[node['id']] = Node(node)

    def __getitem__(self, state_id):
        if state_id in self.nodes:
            return self.nodes.get(state_id)
        else:
            raise AttributeError

    def can_move(self, id_from, id_to, msg_info):
        # TODO: consider whole subtree
        if not id_to in self.nodes[id_from].children:
            return False
        # needed states?
        for entity, val_list in self.nodes[id_to].entities_needed.items():
            if not entity in msg_info:
                return False
            for val in val_list:
                if not val in msg_info[entity]:
                    return False
        # refused states?
        for entity, val_list in self.nodes[id_to].entities_refused.items():
            if len(val_list) == 0:
                if entity in msg_info:
                    return False
            else:
                for val in val_list:
                    if entity in msg_info and val in msg_info[entity]:
                        return False
        return True