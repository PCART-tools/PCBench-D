def test_choice():
    np_dtype = np.random.choice(1, size=()).dtype
    size = (10, 3)
    chunks = 4
    x = da.random.choice(3, size=size, chunks=chunks)
    assert x.dtype == np_dtype
    assert x.shape == size
    res = x.compute()
    assert res.dtype == np_dtype
    assert res.shape == size

    np_a = np.array([1, 3, 5, 7, 9], dtype='f8')
    da_a = da.from_array(np_a, chunks=2)

    for a in [np_a, da_a]:
        x = da.random.choice(a, size=size, chunks=chunks)
        res = x.compute()
        assert x.dtype == np_a.dtype
        assert res.dtype == np_a.dtype
        assert set(np.unique(res)).issubset(np_a)

    np_p = np.array([0, 0.2, 0.2, 0.3, 0.3])
    da_p = da.from_array(np_p, chunks=2)

    for a, p in [(da_a, np_p), (np_a, da_p)]:
        x = da.random.choice(a, size=size, chunks=chunks, p=p)
        res = x.compute()
        assert x.dtype == np_a.dtype
        assert res.dtype == np_a.dtype
        assert set(np.unique(res)).issubset(np_a[1:])

    np_dtype = np.random.choice(1, size=(), p=np.array([1])).dtype
    x = da.random.choice(5, size=size, chunks=chunks, p=np_p)
    res = x.compute()
    assert x.dtype == np_dtype
    assert res.dtype == np_dtype

    errs = [(-1, None),             # negative a
            (np_a[:, None], None),  # a must be 1D
            (np_a, np_p[:, None]),  # p must be 1D
            (np_a, np_p[:-2]),      # a and p must match
            (3, np_p),              # a and p must match
            (4, [0.2, 0.2, 0.3])]   # p must sum to 1

    for (a, p) in errs:
        with pytest.raises(ValueError):
            da.random.choice(a, size=size, chunks=chunks, p=p)

    with pytest.raises(NotImplementedError):
        da.random.choice(da_a, size=size, chunks=chunks, replace=False)

    # Want to make sure replace=False works for a single-partition output array
    x = da.random.choice(da_a, size=da_a.shape[0], chunks=-1, replace=False)
    res = x.compute()
    assert len(res) == len(np.unique(res))
