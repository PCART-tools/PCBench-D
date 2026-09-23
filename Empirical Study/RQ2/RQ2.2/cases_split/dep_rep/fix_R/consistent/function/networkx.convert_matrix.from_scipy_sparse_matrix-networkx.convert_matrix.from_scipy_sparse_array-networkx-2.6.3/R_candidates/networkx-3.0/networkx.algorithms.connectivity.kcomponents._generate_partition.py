def _generate_partition(G, cuts, k):
    def has_nbrs_in_partition(G, node, partition):
        for n in G[node]:
            if n in partition:
                return True
        return False

    components = []
    nodes = {n for n, d in G.degree() if d > k} - {n for cut in cuts for n in cut}
    H = G.subgraph(nodes)
    for cc in nx.connected_components(H):
        component = set(cc)
        for cut in cuts:
            for node in cut:
                if has_nbrs_in_partition(G, node, cc):
                    component.add(node)
        if len(component) < G.order():
            components.append(component)
    yield from _consolidate(components, k + 1)
