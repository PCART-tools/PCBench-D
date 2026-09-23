def _min_cycle(G, orth, weight=None):
    """
    Computes the minimum weight cycle in G,
    orthogonal to the vector orth as per [p. 338, 1]
    """
    T = nx.Graph()

    nodes_idx = {node: idx for idx, node in enumerate(G.nodes())}
    idx_nodes = {idx: node for node, idx in nodes_idx.items()}

    nnodes = len(nodes_idx)

    # Add 2 copies of each edge in G to T. If edge is in orth, add cross edge;
    # otherwise in-plane edge
    for u, v, data in G.edges(data=True):
        uidx, vidx = nodes_idx[u], nodes_idx[v]
        edge_w = data.get(weight, 1)
        if frozenset((u, v)) in orth:
            T.add_edges_from(
                [(uidx, nnodes + vidx), (nnodes + uidx, vidx)], weight=edge_w
            )
        else:
            T.add_edges_from(
                [(uidx, vidx), (nnodes + uidx, nnodes + vidx)], weight=edge_w
            )

    all_shortest_pathlens = dict(nx.shortest_path_length(T, weight=weight))
    cross_paths_w_lens = {
        n: all_shortest_pathlens[n][nnodes + n] for n in range(nnodes)
    }

    # Now compute shortest paths in T, which translates to cyles in G
    start = min(cross_paths_w_lens, key=cross_paths_w_lens.get)
    end = nnodes + start
    min_path = nx.shortest_path(T, source=start, target=end, weight="weight")

    # Now we obtain the actual path, re-map nodes in T to those in G
    min_path_nodes = [node if node < nnodes else node - nnodes for node in min_path]
    # Now remove the edges that occur two times
    mcycle_pruned = _path_to_cycle(min_path_nodes)

    return {frozenset((idx_nodes[u], idx_nodes[v])) for u, v in mcycle_pruned}
