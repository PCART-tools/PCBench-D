def get_outputs(graph):
    for node in graph.find_nodes(op="output"):
        return pytree.tree_leaves(node.args[0])
    raise AssertionError("No output node found")
