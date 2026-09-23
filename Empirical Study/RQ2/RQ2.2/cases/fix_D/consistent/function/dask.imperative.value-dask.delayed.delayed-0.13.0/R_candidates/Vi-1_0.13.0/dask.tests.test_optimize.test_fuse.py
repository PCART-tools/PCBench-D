def test_fuse():
    dsk, dependencies = fuse({'w': (inc, 'x'),
                              'x': (inc, 'y'),
                              'y': (inc, 'z'),
                              'z': (add, 'a', 'b'),
                              'a': 1,
                              'b': 2})
    assert dsk == {'w': (inc, (inc, (inc, (add, 'a', 'b')))),
                   'a': 1,
                   'b': 2}
    assert dependencies == {'a': set(), 'b': set(), 'w': set(['a', 'b'])}
    assert (fuse({'NEW': (inc, 'y'),
                  'w': (inc, 'x'),
                  'x': (inc, 'y'),
                  'y': (inc, 'z'),
                  'z': (add, 'a', 'b'),
                  'a': 1,
                  'b': 2}) ==
            ({'NEW': (inc, 'y'),
              'w': (inc, (inc, 'y')),
              'y': (inc, (add, 'a', 'b')),
              'a': 1,
              'b': 2},
             {'a': set(), 'b': set(), 'y': set(['a', 'b']),
              'w': set(['y']), 'NEW': set(['y'])}))

    assert (fuse({'v': (inc, 'y'),
                  'u': (inc, 'w'),
                  'w': (inc, 'x'),
                  'x': (inc, 'y'),
                  'y': (inc, 'z'),
                  'z': (add, 'a', 'b'),
                  'a': (inc, 'c'),
                  'b': (inc, 'd'),
                  'c': 1,
                  'd': 2}) ==
            ({'u': (inc, (inc, (inc, 'y'))),
              'v': (inc, 'y'),
              'y': (inc, (add, 'a', 'b')),
              'a': (inc, 1),
              'b': (inc, 2)},
             {'a': set(), 'b': set(), 'y': set(['a', 'b']),
              'v': set(['y']), 'u': set(['y'])}))

    assert (fuse({'a': (inc, 'x'),
                  'b': (inc, 'x'),
                  'c': (inc, 'x'),
                  'd': (inc, 'c'),
                  'x': (inc, 'y'),
                  'y': 0}) ==
            ({'a': (inc, 'x'),
              'b': (inc, 'x'),
              'd': (inc, (inc, 'x')),
              'x': (inc, 0)},
             {'x': set(), 'd': set(['x']),
              'a': set(['x']), 'b': set(['x'])}))

    assert (fuse({'a': 1,
                  'b': (inc, 'a'),
                  'c': (add, 'b', 'b')}) ==
            ({'b': (inc, 1),
              'c': (add, 'b', 'b')},
             {'b': set(), 'c': set(['b'])}))
