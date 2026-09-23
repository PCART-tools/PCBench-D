def test_null_graph():
    G = nx.Graph()
    assert not nx.is_biconnected(G)
    assert list(nx.biconnected_components(G)) == []
    assert list(nx.biconnected_component_edges(G)) == []
    assert list(nx.articulation_points(G)) == []
