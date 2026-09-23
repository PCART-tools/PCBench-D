def test_directed():
    with pytest.raises(nx.NetworkXNotImplemented):
        G = nx.gnp_random_graph(10, 0.4, directed=True)
        kc = k_components(G)
