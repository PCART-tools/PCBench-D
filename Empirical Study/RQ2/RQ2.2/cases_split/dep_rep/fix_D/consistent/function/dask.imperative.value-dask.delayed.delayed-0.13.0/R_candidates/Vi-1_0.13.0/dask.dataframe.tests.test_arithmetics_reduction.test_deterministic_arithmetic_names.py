def test_deterministic_arithmetic_names():
    df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [5, 6, 7, 8]})
    a = dd.from_pandas(df, npartitions=2)

    assert sorted((a.x + a.y ** 2).dask) == sorted((a.x + a.y ** 2).dask)
    assert sorted((a.x + a.y ** 2).dask) != sorted((a.x + a.y ** 3).dask)
    assert sorted((a.x + a.y ** 2).dask) != sorted((a.x - a.y ** 2).dask)
