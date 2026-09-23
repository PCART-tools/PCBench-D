def test_directed():
    with pytest.raises(nx.NetworkXNotImplemented):
        G = nx.gnp_random_graph(10, 0.2, directed=True, seed=42)
        nx.k_components(G)
