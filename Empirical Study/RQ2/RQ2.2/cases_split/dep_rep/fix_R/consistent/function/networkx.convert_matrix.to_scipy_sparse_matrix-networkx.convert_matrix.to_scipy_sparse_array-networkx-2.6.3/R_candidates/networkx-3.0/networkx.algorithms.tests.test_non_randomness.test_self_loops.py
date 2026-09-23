def test_self_loops():
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 1)
    with pytest.raises(nx.NetworkXError):
        nx.non_randomness(G)
