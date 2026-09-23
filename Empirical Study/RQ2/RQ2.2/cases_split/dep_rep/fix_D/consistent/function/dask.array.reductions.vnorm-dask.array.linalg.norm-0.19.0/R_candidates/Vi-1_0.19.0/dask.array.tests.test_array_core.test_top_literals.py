def test_top_literals():
    assert top(add, 'z', 'ij', 'x', 'ij', 123, None, numblocks={'x': (2, 2)}) == \
        {('z', 0, 0): (add, ('x', 0, 0), 123),
         ('z', 0, 1): (add, ('x', 0, 1), 123),
         ('z', 1, 0): (add, ('x', 1, 0), 123),
         ('z', 1, 1): (add, ('x', 1, 1), 123)}
