def test_fuse_keys():
    assert (fuse({'a': 1, 'b': (inc, 'a'), 'c': (inc, 'b')}, keys=['b'])
            == ({'b': (inc, 1), 'c': (inc, 'b')},
                {'b': set(), 'c': set(['b'])}))
    dsk, dependencies = fuse({
        'w': (inc, 'x'),
        'x': (inc, 'y'),
        'y': (inc, 'z'),
        'z': (add, 'a', 'b'),
        'a': 1,
        'b': 2,
    }, keys=['x', 'z'])

    assert dsk == {'w': (inc, 'x'),
                   'x': (inc, (inc, 'z')),
                   'z': (add, 'a', 'b'),
                   'a': 1,
                   'b': 2 }
    assert dependencies == {'a': set(), 'b': set(), 'z': set(['a', 'b']),
                            'x': set(['z']), 'w': set(['x'])}
