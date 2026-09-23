def test_random_triad():
    """Tests the random_triad function"""
    G = nx.karate_club_graph()
    G = G.to_directed()
    for i in range(100):
        assert nx.is_triad(nx.random_triad(G))
