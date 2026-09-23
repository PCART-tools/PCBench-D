def test_deep_bases_win_over_dependents():
    """
    d should come before e and probably before one of b and c

            a
          / | \   .
         b  c |
        / \ | /
       e    d
    """
    dsk = {'a': (f, 'b', 'c', 'd'), 'b': (f, 'd', 'e'), 'c': (f, 'd'), 'd': 1,
            'e': 2}

    o = order(dsk)
    assert o['d'] < o['e']
    assert o['d'] < o['b'] or o['d'] < o['c']
