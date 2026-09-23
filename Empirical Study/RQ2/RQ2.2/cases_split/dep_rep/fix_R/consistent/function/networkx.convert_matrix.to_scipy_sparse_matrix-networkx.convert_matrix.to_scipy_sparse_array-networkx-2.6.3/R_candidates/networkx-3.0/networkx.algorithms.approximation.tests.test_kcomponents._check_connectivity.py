def _check_connectivity(G):
    result = k_components(G)
    for k, components in result.items():
        if k < 3:
            continue
        for component in components:
            C = G.subgraph(component)
            K = nx.node_connectivity(C)
            assert K >= k
