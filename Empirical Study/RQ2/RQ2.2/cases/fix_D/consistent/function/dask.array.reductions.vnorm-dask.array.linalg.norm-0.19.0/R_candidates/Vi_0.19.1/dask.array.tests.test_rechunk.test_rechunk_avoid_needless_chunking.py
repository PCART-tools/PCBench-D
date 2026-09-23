def test_rechunk_avoid_needless_chunking():
    x = da.ones(16, chunks=2)
    y = x.rechunk(8)
    dsk = y.__dask_graph__()
    assert len(dsk) <= 8 + 2
