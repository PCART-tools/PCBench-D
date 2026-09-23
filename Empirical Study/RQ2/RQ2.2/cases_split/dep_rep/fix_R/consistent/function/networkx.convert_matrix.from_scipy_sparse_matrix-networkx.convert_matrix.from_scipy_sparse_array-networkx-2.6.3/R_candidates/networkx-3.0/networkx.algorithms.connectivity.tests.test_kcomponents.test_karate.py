def test_karate():
    G = nx.karate_club_graph()
    result = nx.k_components(G)
    _check_connectivity(G, result)
