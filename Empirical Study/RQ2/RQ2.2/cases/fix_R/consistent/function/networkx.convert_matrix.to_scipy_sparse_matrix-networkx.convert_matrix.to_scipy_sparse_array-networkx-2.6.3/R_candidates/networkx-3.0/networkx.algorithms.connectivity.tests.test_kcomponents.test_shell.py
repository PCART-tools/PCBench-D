@pytest.mark.slow
def test_shell():
    constructor = [(20, 80, 0.8), (80, 180, 0.6)]
    G = nx.random_shell_graph(constructor, seed=42)
    result = nx.k_components(G)
    _check_connectivity(G, result)
