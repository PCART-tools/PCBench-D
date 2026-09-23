@pytest.mark.skipif(no_backends_for_leiden_communities)
def test_empty_graph():
    G = nx.Graph()
    G.add_nodes_from(range(5))
    expected = [{0}, {1}, {2}, {3}, {4}]
    assert nx.community.leiden_communities(G) == expected
