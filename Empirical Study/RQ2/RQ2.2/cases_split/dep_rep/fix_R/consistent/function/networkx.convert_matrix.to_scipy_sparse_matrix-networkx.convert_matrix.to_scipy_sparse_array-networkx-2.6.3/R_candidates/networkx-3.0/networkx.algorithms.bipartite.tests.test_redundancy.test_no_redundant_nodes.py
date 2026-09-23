def test_no_redundant_nodes():
    G = complete_bipartite_graph(2, 2)
    rc = node_redundancy(G)
    assert all(redundancy == 1 for redundancy in rc.values())
