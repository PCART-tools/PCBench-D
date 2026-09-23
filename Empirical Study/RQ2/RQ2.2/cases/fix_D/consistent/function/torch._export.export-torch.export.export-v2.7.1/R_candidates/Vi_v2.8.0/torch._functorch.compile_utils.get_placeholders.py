def get_placeholders(graph):
    return graph.find_nodes(op="placeholder")
