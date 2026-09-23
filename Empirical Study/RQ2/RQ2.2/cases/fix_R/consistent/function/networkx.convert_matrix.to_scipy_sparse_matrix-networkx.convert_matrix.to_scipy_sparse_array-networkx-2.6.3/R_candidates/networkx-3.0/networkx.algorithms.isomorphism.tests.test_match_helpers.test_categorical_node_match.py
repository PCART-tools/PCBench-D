def test_categorical_node_match():
    nm = iso.categorical_node_match(["x", "y", "z"], [None] * 3)
    assert nm(dict(x=1, y=2, z=3), dict(x=1, y=2, z=3))
    assert not nm(dict(x=1, y=2, z=2), dict(x=1, y=2, z=1))
