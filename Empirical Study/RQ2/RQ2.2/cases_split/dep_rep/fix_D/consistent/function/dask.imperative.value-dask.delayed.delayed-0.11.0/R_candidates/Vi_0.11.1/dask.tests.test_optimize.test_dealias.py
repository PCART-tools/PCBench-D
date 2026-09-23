def test_dealias():
    dsk = {'a': (range, 5),
           'b': 'a',
           'c': 'b',
           'd': (sum, 'c'),
           'e': 'd',
           'g': 'e',
           'f': (inc, 'd')}

    expected = {'a': (range, 5),
                'd': (sum, 'a'),
                'f': (inc, 'd')}

    assert dealias(dsk) == expected

    dsk = {'a': (range, 5),
           'b': 'a',
           'c': 'a'}

    expected = {'a': (range, 5)}

    assert dealias(dsk) == expected

    dsk = {'a': (inc, 1),
           'b': 'a',
           'c': (inc, 2),
           'd': 'c'}

    assert dealias(dsk) == {'a': (inc, 1),
                            'c': (inc, 2)}

    assert dealias(dsk, keys=['a', 'b', 'd']) == dsk
