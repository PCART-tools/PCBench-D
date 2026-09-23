def get_name_to_node(graph: fx.Graph):
    name_to_node = {}
    for node in graph.nodes:
        name_to_node[node.name] = node
    return name_to_node
