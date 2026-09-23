def test_slicing_with_negative_step_flops_keys():
    x = da.arange(10, chunks=5)
    y = x[:1:-1]
    assert (x.name, 1) in y.dask[(y.name, 0)]
    assert (x.name, 0) in y.dask[(y.name, 1)]

    assert eq(y, np.arange(10)[:1:-1])

    assert y.chunks == ((5, 3),)

    assert y.dask[(y.name, 0)] == (getitem, (x.name, 1),
                                            (slice(-1, -6, -1),))
    assert y.dask[(y.name, 1)] == (getitem, (x.name, 0),
                                            (slice(-1, -4, -1),))
