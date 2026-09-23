def test_has_tasks():
    dsk = {'a': [1, 2, 3],
           'b': 'a',
           'c': [1, (inc, 1)],
           'd': [(sum, 'a')],
           'e': ['a', 'b'],
           'f': [['a', 'b'], 2, 3]}
    assert not has_tasks(dsk, dsk['a'])
    assert has_tasks(dsk, dsk['b'])
    assert has_tasks(dsk, dsk['c'])
    assert has_tasks(dsk, dsk['d'])
    assert has_tasks(dsk, dsk['e'])
    assert has_tasks(dsk, dsk['f'])
