def test_multigraph():
    G = nx.MultiGraph()
    G.add_edge(1, 2, key="first")
    G.add_edge(1, 2, key="second", color="blue")
    H = cytoscape_graph(cytoscape_data(G))
    assert nx.is_isomorphic(G, H)
    assert H[1][2]["second"]["color"] == "blue"
