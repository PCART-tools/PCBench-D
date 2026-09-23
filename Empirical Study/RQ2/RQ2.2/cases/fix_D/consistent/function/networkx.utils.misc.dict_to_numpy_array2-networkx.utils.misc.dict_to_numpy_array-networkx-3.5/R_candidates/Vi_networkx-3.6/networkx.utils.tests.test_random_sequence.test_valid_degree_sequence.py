@pytest.mark.parametrize(
    ("deg_seq", "valid", "reason"),
    [
        ([], False, "must have one more node"),
        ([0], True, ""),
        ([2], False, "must have one more node"),
        ([2, 0], False, "must have strictly positive"),
        ([3, 1, 1, 1], True, ""),
    ],
)
def test_valid_degree_sequence(deg_seq, valid, reason):
    v, r = nx.utils.is_valid_tree_degree_sequence(deg_seq)
    assert v == valid
    assert reason in r
