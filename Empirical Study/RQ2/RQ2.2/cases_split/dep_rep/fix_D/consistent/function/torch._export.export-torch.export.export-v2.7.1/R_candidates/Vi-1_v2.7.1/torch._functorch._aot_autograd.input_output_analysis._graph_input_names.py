def _graph_input_names(gm):
    return [node.name for node in gm.graph.find_nodes(op="placeholder")]
