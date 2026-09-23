def test_graph():
    G = nx.path_graph(4)
    H = cytoscape_graph(cytoscape_data(G))
    assert nx.is_isomorphic(G, H)
