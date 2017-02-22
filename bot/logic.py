from .graph import Graph

def get_msg_info(meaning):
    msg_info = dict()
    for entity, val_list in meaning['entities'].items():
        for val in val_list:
            if not entity in msg_info:
                msg_info[entity] = []
            msg_info[entity].append(val['value'])
    return msg_info

def handle(user_state, meaning, send_fn):
    # TODO: quick reply from response, skip wit
    node_id = user_state.get_state_id()
    valid_children = []
    msg_info = get_msg_info(meaning)
    for child_node_id in graph[node_id].children:
        if graph.can_move(node_id, child_node_id, msg_info):
            valid_children.append(child_node_id)
    # TODO: fix this to consider all valid children
    if len(valid_children) > 0:
        next_child = valid_children[0]
        send_fn(graph[next_child].message)
        return next_child
    else:
        send_fn({ "text": "Nemam pojma" })
        return node_id

graph = Graph()