def test_prefer_deep():
    """
        c
        |
    y   b
    |   |
    x   a

    Prefer longer chains first so we should start with c
    """
    dsk = {'a': 1, 'b': (f, 'a'), 'c': (f, 'b'),
           'x': 1, 'y': (f, 'x')}

    o = order(dsk)
    assert o == {'c': 0, 'b': 1, 'a': 2, 'y': 3, 'x': 4}
