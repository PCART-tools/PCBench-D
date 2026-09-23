def test_getitem_period_str():

    df = pd.DataFrame({'A': np.random.randn(100), 'B': np.random.randn(100)},
                      index=pd.period_range('2011-01-01', freq='H', periods=100))
    ddf = dd.from_pandas(df, 10)

    # partial string slice
    assert eq(df['2011-01-02'],
              ddf['2011-01-02'])
    assert eq(df['2011-01-02':'2011-01-10'],
              df['2011-01-02':'2011-01-10'])
    # same reso, dask result is always DataFrame

    df = pd.DataFrame({'A': np.random.randn(100), 'B': np.random.randn(100)},
                      index=pd.period_range('2011-01-01', freq='D', periods=100))
    ddf = dd.from_pandas(df, 50)
    assert eq(df['2011-01'], ddf['2011-01'])
    assert eq(df['2011'], ddf['2011'])

    assert eq(df['2011-01':'2012-05'], ddf['2011-01':'2012-05'])
    assert eq(df['2011':'2015'], ddf['2011':'2015'])
