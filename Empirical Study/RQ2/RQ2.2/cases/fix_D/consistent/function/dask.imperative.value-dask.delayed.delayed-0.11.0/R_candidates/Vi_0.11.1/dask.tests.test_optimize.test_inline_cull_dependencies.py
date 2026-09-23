def test_inline_cull_dependencies():
    d = {'a': 1,
         'b': 'a',
         'c': 'b',
         'd': ['a', 'b', 'c'],
         'e': (add, (len, 'd'), 'a')}

    d2, dependencies = cull(d, ['d', 'e'])
    inline(d2, {'b'}, dependencies=dependencies)
