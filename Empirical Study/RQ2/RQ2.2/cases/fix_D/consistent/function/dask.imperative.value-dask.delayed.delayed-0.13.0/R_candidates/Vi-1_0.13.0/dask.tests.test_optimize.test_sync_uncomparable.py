def test_sync_uncomparable():
    t1 = Uncomparable()
    t2 = Uncomparable()
    dsk1 = {'a': 1, 'b': t1, 'c': (add, 'a', 'b')}
    dsk2 = {'x': 1, 'y': t2, 'z': (add, 'y', 'x')}
    assert sync_keys(dsk1, dsk2) == {'x': 'a'}

    dsk2 = {'x': 1, 'y': t1, 'z': (add, 'y', 'x')}
    assert sync_keys(dsk1, dsk2) == {'x': 'a', 'y': 'b'}
