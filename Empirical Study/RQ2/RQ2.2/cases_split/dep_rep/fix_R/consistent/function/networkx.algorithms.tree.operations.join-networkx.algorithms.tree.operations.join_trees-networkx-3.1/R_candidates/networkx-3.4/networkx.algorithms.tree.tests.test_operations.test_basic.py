def test_basic():
    """Joining multiple subtrees at a root node."""
    trees = [(nx.full_rary_tree(2, 2**2 - 1), 0) for i in range(2)]
    expected = nx.full_rary_tree(2, 2**3 - 1)
    actual = nx.join_trees(trees, label_attribute="old_labels")
    assert nx.is_isomorphic(actual, expected)
    assert _check_custom_label_attribute(trees, actual, "old_labels")

    actual_without_label = nx.join_trees(trees)
    assert nx.is_isomorphic(actual_without_label, expected)
    # check that no labels were stored
    assert all(not data for _, data in actual_without_label.nodes(data=True))
