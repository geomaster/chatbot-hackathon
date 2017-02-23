from .graph import Graph

def get_wit_info(meaning):
    """Extract valuable information from a Wit meaning object."""
    wit_info = dict()
    for entity, val_list in meaning['entities'].items():
        for val in val_list:
            if not entity in wit_info:
                wit_info[entity] = []
            wit_info[entity].append(val['value'])
    return wit_info

def handle_debug_command(node, msg):
    if msg == '`state?':
        return (node, node or 'None')
    elif msg.startswith('`state='):
        new_node = msg[7:]
        return (new_node, 'Set {0}'.format(new_node))
    return None

def handle(user_state, meaning, send_fn):
    """Do the appropriate state transition for an incoming message.

    Args:
        user_state: A UserState object tied to the user that sent the message. 
        meaning: Wit MessageAPI interpretation of the message. 
        send_fn: A callback used to output bot's response.

    Returns:
        Node ID of a state the user moved to.
    """
    node = user_state.get_state_id()
    if meaning['_text'] and meaning['_text'].startswith('`'):
        debug = handle_debug_command(node, meaning['_text'])
        if debug:
            send_fn({ "text": debug[1] })
            return debug[0]
        else:
            send_fn({ "text": "Nemam pojma tu debug komandu" })
            return node
    wit_info = get_wit_info(meaning)
    valid_next_nodes = graph.get_next(node, wit_info)
    if len(valid_next_nodes) == 1:
        next_node = valid_next_nodes[0]
        send_fn(graph[next_node].message)
        return next_node
    elif len(valid_next_nodes) == 0:
        send_fn({ "text": "Nemam pojma" })
        return node
    else:
        send_fn({ "text": "Nemam pojma (vise resenja)" })
        return node

graph = Graph()
