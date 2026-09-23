def test_mixed_type_union():
    G = nx.Graph()
    H = nx.MultiGraph()
    pytest.raises(nx.NetworkXError, nx.union, G, H)
    pytest.raises(nx.NetworkXError, nx.disjoint_union, G, H)
    pytest.raises(nx.NetworkXError, nx.intersection, G, H)
    pytest.raises(nx.NetworkXError, nx.difference, G, H)
    pytest.raises(nx.NetworkXError, nx.symmetric_difference, G, H)
    pytest.raises(nx.NetworkXError, nx.compose, G, H)
