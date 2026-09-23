def test_make_compound_path_empty():
    # We should be able to make a compound path with no arguments.
    # This makes it easier to write generic path based code.
    r = Path.make_compound_path()
    assert r.vertices.shape == (0, 2)
