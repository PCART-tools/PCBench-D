def test_rolling_function_partition_size():
    df = pd.DataFrame(np.random.randn(50, 2))
    ddf = dd.from_pandas(df, npartitions=5)

    for obj, dobj in [(df, ddf), (df[0], ddf[0])]:
        eq(pd.rolling_mean(obj, 10), dd.rolling_mean(dobj, 10))
        eq(pd.rolling_mean(obj, 11), dd.rolling_mean(dobj, 11))
        raises(NotImplementedError, lambda: dd.rolling_mean(dobj, 12))
