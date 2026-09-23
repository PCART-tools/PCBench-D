def test_finalize_name():
    import dask.array as da
    x = da.ones(10, chunks=5)
    v = delayed([x])
    assert set(x.dask).issubset(v.dask)

    def key(s):
        if isinstance(s, tuple):
            s = s[0]
        return s.split('-')[0]

    assert all(key(k).isalpha() for k in v.dask)
