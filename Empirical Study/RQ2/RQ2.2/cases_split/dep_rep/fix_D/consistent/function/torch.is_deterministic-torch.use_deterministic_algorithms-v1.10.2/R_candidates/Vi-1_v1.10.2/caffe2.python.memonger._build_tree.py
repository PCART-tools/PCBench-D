def _build_tree(paths):
    ''' Build a tree for given paths based on common elements.
        Last elements of all paths are the same, which is the root of the tree.
    '''
    assert all(cp[-1] == paths[0][-1] for cp in paths)
    g = nx.DiGraph()
    node_set = {y for x in paths for y in x}
    g.add_nodes_from(node_set)
    for cp in paths:
        for ce in zip(cp[0:-1], cp[1:]):
            g.add_edge(ce[1], ce[0])

    root = paths[0][-1]
    _compute_tree_height(g, root)

    return (g, root)
