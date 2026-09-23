def test_directed_configuation_model():
    G = nx.directed_configuration_model([], [], seed=0)
    assert len(G) == 0
