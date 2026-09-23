def test_rechunk_with_dict():
    x = da.ones((24, 24), chunks=(4, 8))
    y = x.rechunk(chunks={0: 12})
    assert y.chunks == ((12, 12), (8, 8, 8))

    x = da.ones((24, 24), chunks=(4, 8))
    y = x.rechunk(chunks={0: (12, 12)})
    assert y.chunks == ((12, 12), (8, 8, 8))

    x = da.ones((24, 24), chunks=(4, 8))
    y = x.rechunk(chunks={0: -1})
    assert y.chunks == ((24,), (8, 8, 8))
