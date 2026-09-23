def test_groupby_apply_tasks():
    df = pd.util.testing.makeTimeDataFrame()
    df['A'] = df.A // 0.1
    df['B'] = df.B // 0.1
    ddf = dd.from_pandas(df, npartitions=10)

    with dask.set_options(shuffle='tasks'):
        for ind in [lambda x: 'A', lambda x: x.A]:
            a = df.groupby(ind(df)).apply(len)
            b = ddf.groupby(ind(ddf)).apply(len)
            assert eq(a, b.compute())
            assert not any('partd' in k[0] for k in b.dask)

            a = df.groupby(ind(df)).B.apply(len)
            b = ddf.groupby(ind(ddf)).B.apply(len)
            assert eq(a, b.compute())
            assert not any('partd' in k[0] for k in b.dask)
