def test_rolling_partition_size():
    df = pd.DataFrame(np.random.randn(50, 2))
    ddf = dd.from_pandas(df, npartitions=5)

    for obj, dobj in [(df, ddf), (df[0], ddf[0])]:
        eq(obj.rolling(10).mean(), dobj.rolling(10).mean())
        eq(obj.rolling(11).mean(), dobj.rolling(11).mean())
        raises(NotImplementedError, lambda: dobj.rolling(12).mean())
