def test_compute_v_structures_raise():
    G = nx.Graph()
    pytest.raises(nx.NetworkXNotImplemented, nx.compute_v_structures, G)
