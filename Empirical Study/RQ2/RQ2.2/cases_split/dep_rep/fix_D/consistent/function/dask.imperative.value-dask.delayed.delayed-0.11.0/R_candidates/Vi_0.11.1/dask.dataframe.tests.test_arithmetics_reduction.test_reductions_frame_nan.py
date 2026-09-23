def test_reductions_frame_nan():
    df = pd.DataFrame({'a': [1, 2, np.nan, 4, 5, 6, 7, 8],
                       'b': [1, 2, np.nan, np.nan, np.nan, 5, np.nan, np.nan],
                       'c': [np.nan] * 8})
    ddf = dd.from_pandas(df, 3)
    assert eq(df.sum(), ddf.sum())
    assert eq(df.min(), ddf.min())
    assert eq(df.max(), ddf.max())
    assert eq(df.count(), ddf.count())
    assert eq(df.std(), ddf.std())
    assert eq(df.var(), ddf.var())
    assert eq(df.std(ddof=0), ddf.std(ddof=0))
    assert eq(df.var(ddof=0), ddf.var(ddof=0))
    assert eq(df.mean(), ddf.mean())

    assert eq(df.sum(skipna=False), ddf.sum(skipna=False))
    assert eq(df.min(skipna=False), ddf.min(skipna=False))
    assert eq(df.max(skipna=False), ddf.max(skipna=False))
    assert eq(df.std(skipna=False), ddf.std(skipna=False))
    assert eq(df.var(skipna=False), ddf.var(skipna=False))
    assert eq(df.std(skipna=False, ddof=0), ddf.std(skipna=False, ddof=0))
    assert eq(df.var(skipna=False, ddof=0), ddf.var(skipna=False, ddof=0))
    assert eq(df.mean(skipna=False), ddf.mean(skipna=False))

    assert eq(df.sum(axis=1, skipna=False), ddf.sum(axis=1, skipna=False))
    assert eq(df.min(axis=1, skipna=False), ddf.min(axis=1, skipna=False))
    assert eq(df.max(axis=1, skipna=False), ddf.max(axis=1, skipna=False))
    assert eq(df.std(axis=1, skipna=False), ddf.std(axis=1, skipna=False))
    assert eq(df.var(axis=1, skipna=False), ddf.var(axis=1, skipna=False))
    assert eq(df.std(axis=1, skipna=False, ddof=0),
              ddf.std(axis=1, skipna=False, ddof=0))
    assert eq(df.var(axis=1, skipna=False, ddof=0),
              ddf.var(axis=1, skipna=False, ddof=0))
    assert eq(df.mean(axis=1, skipna=False), ddf.mean(axis=1, skipna=False))

    assert eq(df.cumsum(), ddf.cumsum())
    assert eq(df.cummin(), ddf.cummin())
    assert eq(df.cummax(), ddf.cummax())
    assert eq(df.cumprod(), ddf.cumprod())

    assert eq(df.cumsum(skipna=False), ddf.cumsum(skipna=False))
    assert eq(df.cummin(skipna=False), ddf.cummin(skipna=False))
    assert eq(df.cummax(skipna=False), ddf.cummax(skipna=False))
    assert eq(df.cumprod(skipna=False), ddf.cumprod(skipna=False))

    assert eq(df.cumsum(axis=1), ddf.cumsum(axis=1))
    assert eq(df.cummin(axis=1), ddf.cummin(axis=1))
    assert eq(df.cummax(axis=1), ddf.cummax(axis=1))
    assert eq(df.cumprod(axis=1), ddf.cumprod(axis=1))

    assert eq(df.cumsum(axis=1, skipna=False), ddf.cumsum(axis=1, skipna=False))
    assert eq(df.cummin(axis=1, skipna=False), ddf.cummin(axis=1, skipna=False))
    assert eq(df.cummax(axis=1, skipna=False), ddf.cummax(axis=1, skipna=False))
    assert eq(df.cumprod(axis=1, skipna=False), ddf.cumprod(axis=1, skipna=False))
