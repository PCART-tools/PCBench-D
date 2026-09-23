def test_loc_timestamp_str():

    df = pd.DataFrame({'A': np.random.randn(100), 'B': np.random.randn(100)},
                      index=pd.date_range('2011-01-01', freq='H', periods=100))
    ddf = dd.from_pandas(df, 10)

    # partial string slice
    assert_eq(df.loc['2011-01-02'],
              ddf.loc['2011-01-02'])
    assert_eq(df.loc['2011-01-02':'2011-01-10'],
              ddf.loc['2011-01-02':'2011-01-10'])
    # same reso, dask result is always DataFrame
    assert_eq(df.loc['2011-01-02 10:00'].to_frame().T,
              ddf.loc['2011-01-02 10:00'])

    # series
    assert_eq(df.A.loc['2011-01-02'],
              ddf.A.loc['2011-01-02'])
    assert_eq(df.A.loc['2011-01-02':'2011-01-10'],
              ddf.A.loc['2011-01-02':'2011-01-10'])

    # slice with timestamp (dask result must be DataFrame)
    assert_eq(df.loc[pd.Timestamp('2011-01-02')].to_frame().T,
              ddf.loc[pd.Timestamp('2011-01-02')])
    assert_eq(df.loc[pd.Timestamp('2011-01-02'):pd.Timestamp('2011-01-10')],
              ddf.loc[pd.Timestamp('2011-01-02'):pd.Timestamp('2011-01-10')])
    assert_eq(df.loc[pd.Timestamp('2011-01-02 10:00')].to_frame().T,
              ddf.loc[pd.Timestamp('2011-01-02 10:00')])

    df = pd.DataFrame({'A': np.random.randn(100), 'B': np.random.randn(100)},
                      index=pd.date_range('2011-01-01', freq='M', periods=100))
    ddf = dd.from_pandas(df, 50)
    assert_eq(df.loc['2011-01'], ddf.loc['2011-01'])
    assert_eq(df.loc['2011'], ddf.loc['2011'])

    assert_eq(df.loc['2011-01':'2012-05'], ddf.loc['2011-01':'2012-05'])
    assert_eq(df.loc['2011':'2015'], ddf.loc['2011':'2015'])

    # series
    assert_eq(df.B.loc['2011-01'], ddf.B.loc['2011-01'])
    assert_eq(df.B.loc['2011'], ddf.B.loc['2011'])

    assert_eq(df.B.loc['2011-01':'2012-05'], ddf.B.loc['2011-01':'2012-05'])
    assert_eq(df.B.loc['2011':'2015'], ddf.B.loc['2011':'2015'])
