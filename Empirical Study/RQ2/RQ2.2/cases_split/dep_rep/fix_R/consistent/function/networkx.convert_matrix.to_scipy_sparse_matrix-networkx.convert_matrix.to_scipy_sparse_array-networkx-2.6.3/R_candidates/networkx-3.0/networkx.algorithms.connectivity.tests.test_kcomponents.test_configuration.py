def test_configuration():
    deg_seq = nx.random_powerlaw_tree_sequence(100, tries=5, seed=72)
    G = nx.Graph(nx.configuration_model(deg_seq))
    G.remove_edges_from(nx.selfloop_edges(G))
    result = nx.k_components(G)
    _check_connectivity(G, result)
