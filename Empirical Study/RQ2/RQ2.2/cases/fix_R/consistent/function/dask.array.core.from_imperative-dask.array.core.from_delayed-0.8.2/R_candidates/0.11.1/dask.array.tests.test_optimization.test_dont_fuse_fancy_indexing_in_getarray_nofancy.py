def test_dont_fuse_fancy_indexing_in_getarray_nofancy():
    dsk = {'a': (getitem, (getarray_nofancy, 'x', (slice(10, 20, None), slice(100, 200, None))),
                 ([1, 3], slice(50, 60, None)))}
    assert optimize_slices(dsk) == dsk

    dsk = {'a': (getitem, (getarray_nofancy, 'x', [1, 2, 3]), 0)}
    assert optimize_slices(dsk) == dsk
