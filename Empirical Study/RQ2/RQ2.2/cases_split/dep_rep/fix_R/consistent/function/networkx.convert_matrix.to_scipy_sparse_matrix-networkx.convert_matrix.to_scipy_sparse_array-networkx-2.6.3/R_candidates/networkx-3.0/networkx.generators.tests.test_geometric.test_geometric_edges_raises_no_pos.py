def test_geometric_edges_raises_no_pos():
    G = nx.path_graph(3)
    msg = "All nodes in `G` must have a 'pos' attribute"
    with pytest.raises(nx.NetworkXError, match=msg):
        nx.geometric_edges(G, radius=1)
