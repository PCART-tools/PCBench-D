def test_loc_non_informative_index():
    df = pd.DataFrame({'x': [1, 2, 3, 4]}, index=[10, 20, 30, 40])
    ddf = dd.from_pandas(df, npartitions=2, sort=True)
    ddf.divisions = (None,) * 3
    assert not ddf.known_divisions

    ddf.loc[20:30].compute(get=dask.get)

    assert_eq(ddf.loc[20:30], df.loc[20:30])

    df = pd.DataFrame({'x': [1, 2, 3, 4]}, index=[10, 20, 20, 40])
    ddf = dd.from_pandas(df, npartitions=2, sort=True)
    assert_eq(ddf.loc[20], df.loc[20:20])
