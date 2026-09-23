def test_to_dask_dataframe():
    dd = pytest.importorskip('dask.dataframe')
    a = da.ones((4,), chunks=(2,))
    d = a.to_dask_dataframe()
    assert isinstance(d, dd.Series)

    a = da.ones((4, 4), chunks=(2, 2))
    d = a.to_dask_dataframe()
    assert isinstance(d, dd.DataFrame)
