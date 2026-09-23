def test_karate():
    G = nx.karate_club_graph()
    _check_augmentations(G)
