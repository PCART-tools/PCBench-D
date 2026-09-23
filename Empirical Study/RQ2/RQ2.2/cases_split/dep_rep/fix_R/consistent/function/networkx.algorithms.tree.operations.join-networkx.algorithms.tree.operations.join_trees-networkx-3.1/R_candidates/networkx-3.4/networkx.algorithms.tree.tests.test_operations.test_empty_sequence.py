def test_empty_sequence():
    """Joining the empty sequence results in the tree with one node."""
    T = nx.join_trees([])
    assert len(T) == 1
    assert T.number_of_edges() == 0
