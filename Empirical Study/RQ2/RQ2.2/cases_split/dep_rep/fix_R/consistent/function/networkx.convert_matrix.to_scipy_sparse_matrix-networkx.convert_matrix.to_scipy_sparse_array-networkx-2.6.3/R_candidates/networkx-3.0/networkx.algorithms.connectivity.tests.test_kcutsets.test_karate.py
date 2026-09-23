def test_karate():
    G = nx.karate_club_graph()
    _check_separating_sets(G)
