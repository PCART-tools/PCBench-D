def test_rechunk_unknown_explicit():
    dd = pytest.importorskip('dask.dataframe')
    x = da.ones(shape=(10, 10), chunks=(5, 2))
    y = dd.from_array(x).values
    result = y.rechunk(((float('nan'), float('nan')), (5, 5)))
    expected = x.rechunk((None, (5, 5)))
    assert_chunks_match(result.chunks, expected.chunks)
    assert_eq(result, expected)
