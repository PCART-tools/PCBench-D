def GetPydotGraphMinimal(
    operators_or_net,
    name=None,
    rankdir='LR',
    minimal_dependency=False,
    op_node_producer=None,
):
    """Different from GetPydotGraph, hide all blob nodes and only show op nodes.

    If minimal_dependency is set as well, for each op, we will only draw the
    edges to the minimal necessary ancestors. For example, if op c depends on
    op a and b, and op b depends on a, then only the edge b->c will be drawn
    because a->c will be implied.
    """
    if op_node_producer is None:
        op_node_producer = GetOpNodeProducer(False, **OP_STYLE)
    operators, name = _rectify_operator_and_name(operators_or_net, name)
    graph = pydot.Dot(name, rankdir=rankdir)
    # blob_parents maps each blob name to its generating op.
    blob_parents = {}
    # op_ancestry records the ancestors of each op.
    op_ancestry = defaultdict(set)
    for op_id, op in enumerate(operators):
        op_node = op_node_producer(op, op_id)
        graph.add_node(op_node)
        # Get parents, and set up op ancestry.
        parents = [
            blob_parents[input_name] for input_name in op.input
            if input_name in blob_parents
        ]
        op_ancestry[op_node].update(parents)
        for node in parents:
            op_ancestry[op_node].update(op_ancestry[node])
        if minimal_dependency:
            # only add nodes that do not have transitive ancestry
            for node in parents:
                if all(
                    [node not in op_ancestry[other_node]
                     for other_node in parents]
                ):
                    graph.add_edge(pydot.Edge(node, op_node))
        else:
            # Add all parents to the graph.
            for node in parents:
                graph.add_edge(pydot.Edge(node, op_node))
        # Update blob_parents to reflect that this op created the blobs.
        for output_name in op.output:
            blob_parents[output_name] = op_node
    return graph
