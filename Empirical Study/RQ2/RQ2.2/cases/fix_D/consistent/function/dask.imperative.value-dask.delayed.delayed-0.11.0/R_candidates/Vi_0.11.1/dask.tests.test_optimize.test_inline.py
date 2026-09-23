def test_inline():
    d = {'a': 1,
         'b': (inc, 'a'),
         'c': (inc, 'b'),
         'd': (add, 'a', 'c')}
    assert inline(d) == {'a': 1,
                         'b': (inc, 1),
                         'c': (inc, 'b'),
                         'd': (add, 1, 'c')}
    assert inline(d, ['a', 'b', 'c']) == {'a': 1,
                                          'b': (inc, 1),
                                          'c': (inc, (inc, 1)),
                                          'd': (add, 1, (inc, (inc, 1)))}
    d = {'x': 1,
         'y': (inc, 'x'),
         'z': (add, 'x', 'y')}
    assert inline(d) == {'x': 1,
                         'y': (inc, 1),
                         'z': (add, 1, 'y')}
    assert inline(d, keys='y') == {'x': 1,
                                   'y': (inc, 1),
                                   'z': (add, 1, (inc, 1))}
    assert inline(d, keys='y',
                  inline_constants=False) == {'x': 1,
                                              'y': (inc, 'x'),
                                              'z': (add, 'x', (inc, 'x'))}

    d = {'a': 1,
         'b': 'a',
         'c': 'b',
         'd': ['a', 'b', 'c'],
         'e': (add, (len, 'd'), 'a')}
    assert inline(d, 'd') == {'a': 1,
                              'b': 1,
                              'c': 1,
                              'd': [1, 1, 1],
                              'e': (add, (len, [1, 1, 1]), 1)}
    assert inline(d, 'a',
                  inline_constants=False) == {'a': 1,
                                              'b': 1,
                                              'c': 'b',
                                              'd': [1, 'b', 'c'],
                                              'e': (add, (len, 'd'), 1)}
