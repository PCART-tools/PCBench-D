def test_rechunk_unknown_from_array():
    dd = pytest.importorskip('dask.dataframe')
    # pd = pytest.importorskip('pandas')
    x = dd.from_array(da.ones(shape=(4, 4), chunks=(2, 2))).values
    # result = x.rechunk({1: 5})
    result = x.rechunk((None, 4))
    assert np.isnan(x.chunks[0]).all()
    assert np.isnan(result.chunks[0]).all()
    assert x.chunks[1] == (4,)
    assert_eq(x, result)
