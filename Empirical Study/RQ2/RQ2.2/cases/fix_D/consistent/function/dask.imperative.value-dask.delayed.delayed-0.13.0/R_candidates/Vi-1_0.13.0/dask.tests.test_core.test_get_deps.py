def test_get_deps():
    """
    >>> dsk = {'a': 1, 'b': (inc, 'a'), 'c': (inc, 'b')}
    >>> dependencies, dependents = get_deps(dsk)
    >>> dependencies
    {'a': set([]), 'c': set(['b']), 'b': set(['a'])}
    >>> dependents
    {'a': set(['b']), 'c': set([]), 'b': set(['c'])}
    """
    dsk = {'a': [1, 2, 3],
           'b': 'a',
           'c': [1, (inc, 1)],
           'd': [(sum, 'c')],
           'e': ['b', 'zzz', 'b'],
           'f': [['a', 'b'], 2, 3]}
    dependencies, dependents = get_deps(dsk)
    assert dependencies == {'a': set(),
                            'b': {'a'},
                            'c': set(),
                            'd': {'c'},
                            'e': {'b'},
                            'f': {'a', 'b'},
                            }
    assert dependents == {'a': {'b', 'f'},
                          'b': {'e', 'f'},
                          'c': {'d'},
                          'd': set(),
                          'e': set(),
                          'f': set(),
                          }
