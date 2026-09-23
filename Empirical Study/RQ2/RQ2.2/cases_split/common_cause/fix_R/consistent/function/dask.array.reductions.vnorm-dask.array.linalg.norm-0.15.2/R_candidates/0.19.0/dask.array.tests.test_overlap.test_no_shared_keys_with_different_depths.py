def test_no_shared_keys_with_different_depths():
    da.random.seed(0)
    a = da.random.random((9, 9), chunks=(3, 3))

    def check(x):
        assert x.shape == (3, 3)
        return x

    r = [a.map_overlap(lambda a: a + 1,
                       dtype=a.dtype,
                       depth={j: int(i == j) for j in range(a.ndim)},
                       boundary="none").map_blocks(check, dtype=a.dtype)
         for i in range(a.ndim)]

    assert set(r[0].dask) & set(r[1].dask) == set(a.dask)
    da.compute(*r, scheduler='single-threaded')
