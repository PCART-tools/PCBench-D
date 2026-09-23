@pytest.mark.slow
def test_random_gnp():
    G = nx.gnp_random_graph(50, 0.2, seed=42)
    result = nx.k_components(G)
    _check_connectivity(G, result)
