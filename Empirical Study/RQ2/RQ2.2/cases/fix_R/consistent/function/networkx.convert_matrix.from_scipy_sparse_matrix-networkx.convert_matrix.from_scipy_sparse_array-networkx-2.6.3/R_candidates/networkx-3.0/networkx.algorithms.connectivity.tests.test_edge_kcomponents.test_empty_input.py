def test_empty_input():
    G = nx.Graph()
    assert [] == list(nx.k_edge_components(G, k=5))
    assert [] == list(nx.k_edge_subgraphs(G, k=5))

    G = nx.DiGraph()
    assert [] == list(nx.k_edge_components(G, k=5))
    assert [] == list(nx.k_edge_subgraphs(G, k=5))
