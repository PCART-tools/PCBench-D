def test_optimize_slicing():
    dsk = {'a': (range, 10),
           'b': (getter, 'a', (slice(None, None, None),)),
           'c': (getter, 'b', (slice(None, None, None),)),
           'd': (getter, 'c', (slice(0, 5, None),)),
           'e': (getter, 'd', (slice(None, None, None),))}

    expected = {'e': (getter, (range, 10), (slice(0, 5, None),))}
    result = optimize_slices(fuse(dsk, [], rename_keys=False)[0])
    assert result == expected

    # protect output keys
    expected = {'c': (getter, (range, 10), (slice(0, None, None),)),
                'd': (getter, 'c', (slice(0, 5, None),)),
                'e': (getter, 'd', (slice(None, None, None),))}
    result = optimize_slices(fuse(dsk, ['c', 'd', 'e'], rename_keys=False)[0])

    assert result == expected
