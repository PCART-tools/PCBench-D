def test_rechunk_warning():
    N = 20
    x = da.random.normal(size=(N, N, 100), chunks=(1, N, 100))
    with warnings.catch_warnings(record=True) as w:
        x = x.rechunk((N, 1, 100))

    assert not w
