def test_mixed_type_intersection():
    with pytest.raises(nx.NetworkXError):
        G = nx.Graph()
        H = nx.MultiGraph()
        I = nx.Graph()
        U = nx.intersection_all([G, H, I])
