def test_fuse_keys():
    d = {
        'a': 1,
        'b': (inc, 'a'),
        'c': (inc, 'b'),
    }
    keys = ['b']
    dsk, dependencies = fuse(d, keys, rename_fused_keys=False)
    assert dsk == {
        'b': (inc, 1),
        'c': (inc, 'b'),
    }
    assert dependencies == {'b': set(), 'c': set(['b'])}

    dsk, dependencies = fuse(d, keys, rename_fused_keys=True)
    assert dsk == {
        'a-b': (inc, 1),
        'c': (inc, 'a-b'),
        'b': 'a-b',
    }
    assert dependencies == {'a-b': set(), 'c': set(['a-b']), 'b': set(['a-b'])}

    d = {
        'w': (inc, 'x'),
        'x': (inc, 'y'),
        'y': (inc, 'z'),
        'z': (add, 'a', 'b'),
        'a': 1,
        'b': 2,
    }
    keys = ['x', 'z']
    dsk, dependencies = fuse(d, keys, rename_fused_keys=False)
    assert dsk == {
        'w': (inc, 'x'),
        'x': (inc, (inc, 'z')),
        'z': (add, 'a', 'b'),
        'a': 1,
        'b': 2 ,
    }
    assert dependencies == {'a': set(), 'b': set(), 'z': set(['a', 'b']),
                            'x': set(['z']), 'w': set(['x'])}

    dsk, dependencies = fuse(d, keys, rename_fused_keys=True)
    assert dsk == {
        'w': (inc, 'y-x'),
        'y-x': (inc, (inc, 'z')),
        'z': (add, 'a', 'b'),
        'a': 1,
        'b': 2 ,
        'x': 'y-x',
    }
    assert dependencies == {'a': set(), 'b': set(), 'z': set(['a', 'b']),
                            'y-x': set(['z']), 'w': set(['y-x']),
                            'x': set(['y-x'])}
