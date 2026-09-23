def test_rechunk_unknown_raises():
    dd = pytest.importorskip('dask.dataframe')

    x = dd.from_array(da.ones(shape=(10, 10), chunks=(5, 5))).values
    with pytest.raises(ValueError):
        x.rechunk((None, (5, 5, 5)))
