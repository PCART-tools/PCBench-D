def test_index_with_dask_array_errors():
    x = da.ones((5, 5), chunks=2)
    with pytest.raises(NotImplementedError):
        x[0, x > 10]
