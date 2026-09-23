def test_exceptions():
    """Bad input should raise exception."""
    G = nx.florentine_families_graph()
    pytest.raises(nx.NetworkXUnfeasible, nx.maximal_independent_set, G, ["Smith"])
    pytest.raises(
        nx.NetworkXUnfeasible, nx.maximal_independent_set, G, ["Salviati", "Pazzi"]
    )
    # MaximalIndependantSet is not implemented for directed graphs
    pytest.raises(nx.NetworkXNotImplemented, nx.maximal_independent_set, nx.DiGraph(G))
