def test_raise_on_no_chunks():
    x = da.ones(6, chunks=3)
    try:
        Array(x.dask, x.name, chunks=None, dtype=x.dtype, shape=None)
        assert False
    except ValueError as e:
        assert "dask.pydata.org" in str(e)

    pytest.raises(ValueError, lambda: da.ones(6))
