def test_merge_sync():
    dsk1 = {'a': 1, 'b': (add, 'a', 10), 'c': (mul, 'b', 5)}
    dsk2 = {'x': 1, 'y': (add, 'x', 10), 'z': (mul, 'y', 2)}
    new_dsk, key_map = merge_sync(dsk1, dsk2)
    assert new_dsk == {'a': 1, 'b': (add, 'a', 10), 'c': (mul, 'b', 5),
            'z': (mul, 'b', 2)}
    assert key_map == {'x': 'a', 'y': 'b', 'z': 'z'}

    dsk1 = {'g1': 1,
            'g2': 2,
            'g3': (add, 'g1', 1),
            'g4': (add, 'g2', 1),
            'g5': (mul, (inc, 'g3'), (inc, 'g4'))}
    dsk2 = {'h1': 1,
            'h2': 5,
            'h3': (add, 'h1', 1),
            'h4': (add, 'h2', 1),
            'h5': (mul, (inc, 'h3'), (inc, 'h4'))}
    new_dsk, key_map = merge_sync(dsk1, dsk2)
    assert new_dsk == {'g1': 1,
                       'g2': 2,
                       'g3': (add, 'g1', 1),
                       'g4': (add, 'g2', 1),
                       'g5': (mul, (inc, 'g3'), (inc, 'g4')),
                       'h2': 5,
                       'h4': (add, 'h2', 1),
                       'h5': (mul, (inc, 'g3'), (inc, 'h4'))}
    assert key_map == {'h1': 'g1', 'h2': 'h2', 'h3': 'g3',
            'h4': 'h4', 'h5': 'h5'}

    # Test merging with name conflict
    # Reset name count to ensure same numbers
    merge_sync.names = ("merge_%d" % i for i in count(1))
    dsk1 = {'g1': 1, 'conflict': (add, 'g1', 2), 'g2': (add, 'conflict', 3)}
    dsk2 = {'h1': 1, 'conflict': (add, 'h1', 4), 'h2': (add, 'conflict', 3)}
    new_dsk, key_map = merge_sync(dsk1, dsk2)
    assert new_dsk == {'g1': 1,
                       'conflict': (add, 'g1', 2),
                       'merge_1': (add, 'g1', 4),
                       'g2': (add, 'conflict', 3),
                       'h2': (add, 'merge_1', 3)}
    assert key_map == {'h1': 'g1', 'conflict': 'merge_1', 'h2': 'h2'}
