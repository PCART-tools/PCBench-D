def test_multidigraph():
    G = nx.MultiDiGraph()
    nx.add_path(G, [1, 2, 3])
    H = cytoscape_graph(cytoscape_data(G))
    assert H.is_directed()
    assert H.is_multigraph()
