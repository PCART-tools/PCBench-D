def test_fuse():
    d = {
        'w': (inc, 'x'),
        'x': (inc, 'y'),
        'y': (inc, 'z'),
        'z': (add, 'a', 'b'),
        'a': 1,
        'b': 2,
    }
    dsk, dependencies = fuse(d, rename_fused_keys=False)
    assert dsk == {
        'w': (inc, (inc, (inc, (add, 'a', 'b')))),
        'a': 1,
        'b': 2,
    }
    assert dependencies == {'a': set(), 'b': set(), 'w': set(['a', 'b'])}

    dsk, dependencies = fuse(d, rename_fused_keys=True)
    assert dsk == {
        'z-y-x-w': (inc, (inc, (inc, (add, 'a', 'b')))),
        'a': 1,
        'b': 2,
        'w': 'z-y-x-w',
    }
    assert dependencies == {'a': set(), 'b': set(), 'z-y-x-w': set(['a', 'b']),
                            'w': set(['z-y-x-w'])}

    d = {
        'NEW': (inc, 'y'),
        'w': (inc, 'x'),
        'x': (inc, 'y'),
        'y': (inc, 'z'),
        'z': (add, 'a', 'b'),
        'a': 1,
        'b': 2,
    }
    dsk, dependencies = fuse(d, rename_fused_keys=False)
    assert dsk == {
        'NEW': (inc, 'y'),
        'w': (inc, (inc, 'y')),
        'y': (inc, (add, 'a', 'b')),
        'a': 1,
        'b': 2,
    }
    assert dependencies == {'a': set(), 'b': set(), 'y': set(['a', 'b']),
                            'w': set(['y']), 'NEW': set(['y'])}

    dsk, dependencies = fuse(d, rename_fused_keys=True)
    assert dsk == {
        'NEW': (inc, 'z-y'),
        'x-w': (inc, (inc, 'z-y')),
        'z-y': (inc, (add, 'a', 'b')),
        'a': 1,
        'b': 2,
        'w': 'x-w',
        'y': 'z-y',
    }
    assert dependencies == {'a': set(), 'b': set(), 'z-y': set(['a', 'b']),
                            'x-w': set(['z-y']), 'NEW': set(['z-y']),
                            'w': set(['x-w']), 'y': set(['z-y'])}

    d = {
        'v': (inc, 'y'),
        'u': (inc, 'w'),
        'w': (inc, 'x'),
        'x': (inc, 'y'),
        'y': (inc, 'z'),
        'z': (add, 'a', 'b'),
        'a': (inc, 'c'),
        'b': (inc, 'd'),
        'c': 1,
        'd': 2,
    }
    dsk, dependencies = fuse(d, rename_fused_keys=False)
    assert dsk == {
        'u': (inc, (inc, (inc, 'y'))),
        'v': (inc, 'y'),
        'y': (inc, (add, 'a', 'b')),
        'a': (inc, 1),
        'b': (inc, 2),
    }
    assert dependencies == {'a': set(), 'b': set(), 'y': set(['a', 'b']),
                            'v': set(['y']), 'u': set(['y'])}

    dsk, dependencies = fuse(d, rename_fused_keys=True)
    assert dsk == {
        'x-w-u': (inc, (inc, (inc, 'z-y'))),
        'v': (inc, 'z-y'),
        'z-y': (inc, (add, 'c-a', 'd-b')),
        'c-a': (inc, 1),
        'd-b': (inc, 2),
        'a': 'c-a',
        'b': 'd-b',
        'u': 'x-w-u',
        'y': 'z-y',
    }
    assert dependencies == {
        'c-a': set(),
        'd-b': set(),
        'z-y': set(['c-a', 'd-b']),
        'v': set(['z-y']),
        'x-w-u': set(['z-y']),
        'a': set(['c-a']),
        'b': set(['d-b']),
        'u': set(['x-w-u']),
        'y': set(['z-y']),
    }

    d = {
        'a': (inc, 'x'),
        'b': (inc, 'x'),
        'c': (inc, 'x'),
        'd': (inc, 'c'),
        'x': (inc, 'y'),
        'y': 0,
    }
    dsk, dependencies = fuse(d, rename_fused_keys=False)
    assert dsk == {
        'a': (inc, 'x'),
        'b': (inc, 'x'),
        'd': (inc, (inc, 'x')),
        'x': (inc, 0)
    }
    assert dependencies == {'x': set(), 'd': set(['x']),
                            'a': set(['x']), 'b': set(['x'])}

    dsk, dependencies = fuse(d, rename_fused_keys=True)
    assert dsk == {
        'a': (inc, 'y-x'),
        'b': (inc, 'y-x'),
        'c-d': (inc, (inc, 'y-x')),
        'y-x': (inc, 0),
        'd': 'c-d',
        'x': 'y-x',
    }
    assert dependencies == {'y-x': set(), 'c-d': set(['y-x']),
                            'a': set(['y-x']), 'b': set(['y-x']),
                            'd': set(['c-d']), 'x': set(['y-x'])}

    d = {
        'a': 1,
        'b': (inc, 'a'),
        'c': (add, 'b', 'b'),
    }
    dsk, dependencies = fuse(d, rename_fused_keys=False)
    assert dsk == {
        'b': (inc, 1),
        'c': (add, 'b', 'b'),
    }
    assert dependencies == {'b': set(), 'c': set(['b'])}

    dsk, dependencies = fuse(d, rename_fused_keys=True)
    assert dsk == {
        'a-b': (inc, 1),
        'c': (add, 'a-b', 'a-b'),
        'b': 'a-b',
    }
    assert dependencies == {'a-b': set(), 'c': set(['a-b']), 'b': set(['a-b'])}
