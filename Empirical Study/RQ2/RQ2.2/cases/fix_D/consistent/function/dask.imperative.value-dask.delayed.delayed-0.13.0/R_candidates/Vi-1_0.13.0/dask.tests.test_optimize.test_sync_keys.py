def test_sync_keys():
    dsk1 = {'a': 1, 'b': (add, 'a', 10), 'c': (mul, 'b', 5)}
    dsk2 = {'x': 1, 'y': (add, 'x', 10), 'z': (mul, 'y', 2)}
    assert sync_keys(dsk1, dsk2) == {'x': 'a', 'y': 'b'}
    assert sync_keys(dsk2, dsk1) == {'a': 'x', 'b': 'y'}

    dsk1 = {'a': 1, 'b': 2, 'c': (add, 'a', 'b'), 'd': (inc, (add, 'a', 'b'))}
    dsk2 = {'x': 1, 'y': 5, 'z': (add, 'x', 'y'), 'w': (inc, (add, 'x', 'y'))}
    assert sync_keys(dsk1, dsk2) == {'x': 'a'}
    assert sync_keys(dsk2, dsk1) == {'a': 'x'}
