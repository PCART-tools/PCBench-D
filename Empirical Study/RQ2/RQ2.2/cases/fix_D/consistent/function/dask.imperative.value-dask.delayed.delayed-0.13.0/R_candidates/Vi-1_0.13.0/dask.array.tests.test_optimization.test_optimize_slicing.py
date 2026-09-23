def test_optimize_slicing():
    dsk = {'a': (range, 10),
           'b': (getarray, 'a', (slice(None, None, None),)),
           'c': (getarray, 'b', (slice(None, None, None),)),
           'd': (getarray, 'c', (slice(0, 5, None),)),
           'e': (getarray, 'd', (slice(None, None, None),))}

    expected = {'e': (getarray, (range, 10), (slice(0, 5, None),))}
    result = optimize_slices(fuse(dsk, [])[0])
    assert result == expected

    # protect output keys
    expected = {'c': (getarray, (range, 10), (slice(0, None, None),)),
                'd': (getarray, 'c', (slice(0, 5, None),)),
                'e': (getarray, 'd', (slice(None, None, None),))}
    result = optimize_slices(fuse(dsk, ['c', 'd', 'e'])[0])

    assert result == expected
