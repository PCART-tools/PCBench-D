def dorogovtsev_goltsev_mendes_graph(n, create_using=None):
    """Returns the hierarchically constructed Dorogovtsev-Goltsev-Mendes graph.

    n is the generation.
    See: arXiv:/cond-mat/0112143 by Dorogovtsev, Goltsev and Mendes.

    """
    G = empty_graph(0, create_using)
    if G.is_directed():
        raise NetworkXError("Directed Graph not supported")
    if G.is_multigraph():
        raise NetworkXError("Multigraph not supported")

    G.add_edge(0, 1)
    if n == 0:
        return G
    new_node = 2  # next node to be added
    for i in range(1, n + 1):  # iterate over number of generations.
        last_generation_edges = list(G.edges())
        number_of_edges_in_last_generation = len(last_generation_edges)
        for j in range(0, number_of_edges_in_last_generation):
            G.add_edge(new_node, last_generation_edges[j][0])
            G.add_edge(new_node, last_generation_edges[j][1])
            new_node += 1
    return G
