def test_rechunk_unknown_from_pandas():
    dd = pytest.importorskip('dask.dataframe')
    pd = pytest.importorskip('pandas')

    arr = np.random.randn(50, 10)
    x = dd.from_pandas(pd.DataFrame(arr), 2).values
    result = x.rechunk((None, (5, 5)))
    assert np.isnan(x.chunks[0]).all()
    assert np.isnan(result.chunks[0]).all()
    assert result.chunks[1] == (5, 5)
    expected = da.from_array(arr, chunks=((25, 25), (10,))).rechunk((None, (5, 5)))
    assert_eq(result, expected)
