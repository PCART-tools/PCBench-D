def test_non_connected():
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_node(3)
    with pytest.raises(nx.NetworkXException):
        nx.non_randomness(G)
