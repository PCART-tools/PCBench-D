def test_mixed_type_disjoint_union():
    with pytest.raises(nx.NetworkXError):
        G = nx.Graph()
        H = nx.MultiGraph()
        I = nx.Graph()
        U = nx.disjoint_union_all([G, H, I])
