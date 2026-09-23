def test_hard_fuse_slice_cases():
    dsk = {'x': (getter, (getter, 'x', (None, slice(None, None))),
                 (slice(None, None), 5))}
    assert optimize_slices(dsk) == {'x': (getter, 'x', (None, 5))}
