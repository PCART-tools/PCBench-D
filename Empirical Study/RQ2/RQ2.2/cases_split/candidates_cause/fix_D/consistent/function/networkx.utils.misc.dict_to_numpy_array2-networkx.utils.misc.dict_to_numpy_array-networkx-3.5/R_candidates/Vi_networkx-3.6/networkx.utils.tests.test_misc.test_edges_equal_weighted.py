@pytest.mark.parametrize("n", [5, 10, 20])
@pytest.mark.parametrize("gen", [nx.complete_graph, nx.path_graph, nx.cycle_graph])
@pytest.mark.parametrize("weight", [1, 2, 3])
def test_edges_equal_weighted(n, gen, weight):
    """Test whether ``edges_equal`` properly compares edges with weight data."""
    G = gen(n)
    H = gen(n)

    G_edges = list(G.edges())
    G.add_weighted_edges_from((*e, weight) for e in G_edges)
    assert edges_equal(G.edges(), G.edges())

    H.add_weighted_edges_from((*e, weight + 1) for e in G_edges)
    assert edges_equal(H.edges(), H.edges())
    assert not edges_equal(G.edges(data=True), H.edges(data=True))
