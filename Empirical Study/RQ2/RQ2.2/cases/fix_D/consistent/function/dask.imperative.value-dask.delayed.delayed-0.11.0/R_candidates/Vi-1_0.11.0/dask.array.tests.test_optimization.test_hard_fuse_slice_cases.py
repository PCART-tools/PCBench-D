def test_hard_fuse_slice_cases():
    dsk = {'x': (getarray, (getarray, 'x', (None, slice(None, None))),
                     (slice(None, None), 5))}
    assert optimize_slices(dsk) == {'x': (getarray, 'x', (None, 5))}
