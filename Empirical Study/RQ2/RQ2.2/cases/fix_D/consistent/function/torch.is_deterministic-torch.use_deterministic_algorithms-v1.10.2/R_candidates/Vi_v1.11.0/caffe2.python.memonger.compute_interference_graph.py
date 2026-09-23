def compute_interference_graph(ops):
    g = nx.DiGraph()
    for i, op in enumerate(ops):
        g.add_node(i, op=op)
    for i, parent_op in enumerate(ops):
        for j, child_op in enumerate(ops):
            if i >= j:
                continue
            if any(output in child_op.input for output in parent_op.output):
                deps = set(child_op.input).intersection(parent_op.output)
                g.add_edge(i, j, deps=deps)
                assert nx.is_directed_acyclic_graph(g), child_op
    return g
