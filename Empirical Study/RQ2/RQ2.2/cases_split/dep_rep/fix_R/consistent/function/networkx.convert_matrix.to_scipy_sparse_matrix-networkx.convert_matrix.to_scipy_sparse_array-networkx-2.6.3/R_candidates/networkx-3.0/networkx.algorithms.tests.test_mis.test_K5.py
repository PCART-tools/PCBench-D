@pytest.mark.parametrize("graph", [nx.complete_graph(5), nx.complete_graph(55)])
def test_K5(graph):
    """Maximal independent set for complete graphs"""
    assert all(nx.maximal_independent_set(graph, [n]) == [n] for n in graph)
