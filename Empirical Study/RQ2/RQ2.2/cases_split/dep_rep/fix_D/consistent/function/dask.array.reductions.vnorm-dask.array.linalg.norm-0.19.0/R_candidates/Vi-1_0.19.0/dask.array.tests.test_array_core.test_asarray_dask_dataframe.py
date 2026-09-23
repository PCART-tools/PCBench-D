def test_asarray_dask_dataframe():
    # https://github.com/dask/dask/issues/3885
    dd = pytest.importorskip('dask.dataframe')
    import pandas as pd

    s = dd.from_pandas(pd.Series([1, 2, 3, 4]), 2)
    result = da.asarray(s)
    expected = s.values
    assert_eq(result, expected)

    df = s.to_frame(name='s')
    result = da.asarray(df)
    expected = df.values
    assert_eq(result, expected)
