@pytest.mark.xfail
def test_cull():
    x = da.ones(1000, chunks=(10,))

    for slc in [1, slice(0, 30), slice(0, None, 100)]:
        y = x[slc]
        assert len(y.dask) < len(x.dask)
