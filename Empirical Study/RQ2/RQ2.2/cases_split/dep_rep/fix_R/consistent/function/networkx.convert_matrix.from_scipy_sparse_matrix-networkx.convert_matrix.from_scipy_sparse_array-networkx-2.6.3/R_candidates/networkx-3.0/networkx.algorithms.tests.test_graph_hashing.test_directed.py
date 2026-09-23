def test_directed():
    """
    A directed graph with no bi-directional edges should yield different a graph hash
    to the same graph taken as undirected if there are no hash collisions.
    """
    r = 10
    for i in range(r):
        G_directed = nx.gn_graph(10 + r, seed=100 + i)
        G_undirected = nx.to_undirected(G_directed)

        h_directed = nx.weisfeiler_lehman_graph_hash(G_directed)
        h_undirected = nx.weisfeiler_lehman_graph_hash(G_undirected)

        assert h_directed != h_undirected
