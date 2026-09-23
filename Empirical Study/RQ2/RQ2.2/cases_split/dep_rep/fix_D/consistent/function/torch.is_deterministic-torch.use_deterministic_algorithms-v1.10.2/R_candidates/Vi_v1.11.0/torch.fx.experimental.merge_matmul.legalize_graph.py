def legalize_graph(gm: GraphModule):
    """
    Replace the graph of the given GraphModule with one that contains the same nodes as the
    original, but in topologically sorted order.

    This is used by the merge_matmul transformation below, which disturbs the topologically sorted
    order of its input GraphModule, so that this order is restored before further transformation.

    Arguments:
        gm: The graph module to topologically sort. It is modified in-place.

    """
    # Build an adjacency list representation of node dependencies in the graph. This also
    # serves as a list of nodes that still need to be inserted into the new, topologically
    # sorted graph.
    dependencies = {node: node.all_input_nodes.copy() for node in gm.graph.nodes}

    # Construct a new graph that will contain all nodes in topologically sorted order.
    new_graph = Graph()
    value_remap: Dict[Node, Node] = {}

    # Copy over all nodes with no dependencies.
    for node, deps in dependencies.items():
        if not deps:
            value_remap[node] = new_graph.node_copy(node, lambda n: value_remap[n])

    # Remove the copied over nodes from the adjacency list.
    for copied_node in value_remap.keys():
        del dependencies[copied_node]

    # While there are still nodes to insert into the new graph:
    while dependencies:
        copied_this_round = []

        # Copy over all nodes whose dependencies already exist in the new graph.
        for node, deps in dependencies.items():
            all_deps_copied = True
            for dep in deps:
                if dep not in value_remap:
                    all_deps_copied = False

            if all_deps_copied:
                value_remap[node] = new_graph.node_copy(node, lambda n: value_remap[n])
                copied_this_round.append(node)

        # Delete all nodes copied over in this iteration from dependencies.
        for copied_node in copied_this_round:
            del dependencies[copied_node]

    # Replace the old graph with the new, topologically sorted one.
    gm.graph = new_graph
