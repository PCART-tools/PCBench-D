def test_is_aperiodic_raise():
    G = nx.Graph()
    pytest.raises(nx.NetworkXError, nx.is_aperiodic, G)
