def test_rolling_axis():
    df = pd.DataFrame(np.random.randn(20, 16))
    ddf = dd.from_pandas(df, npartitions=3)

    assert_eq(df.rolling(3, axis=0).mean(), ddf.rolling(3, axis=0).mean())
    assert_eq(df.rolling(3, axis=1).mean(), ddf.rolling(3, axis=1).mean())
    assert_eq(df.rolling(3, min_periods=1, axis=1).mean(),
              ddf.rolling(3, min_periods=1, axis=1).mean())
    assert_eq(df.rolling(3, axis='columns').mean(),
              ddf.rolling(3, axis='columns').mean())
    assert_eq(df.rolling(3, axis='rows').mean(),
              ddf.rolling(3, axis='rows').mean())

    s = df[3]
    ds = ddf[3]
    assert_eq(s.rolling(5, axis=0).std(), ds.rolling(5, axis=0).std())
