def _check_connectivity(G, k_components):
    for k, components in k_components.items():
        if k < 3:
            continue
        # check that k-components have node connectivity >= k.
        for component in components:
            C = G.subgraph(component)
            K = nx.node_connectivity(C)
            assert K >= k
