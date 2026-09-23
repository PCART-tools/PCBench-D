def test_meta_nonempty():
    df1 = pd.DataFrame({'A': pd.Categorical(['Alice', 'Bob', 'Carol']),
                        'B': list('abc'),
                        'C': 'bar',
                        'D': 3.0,
                        'E': pd.Timestamp('2016-01-01'),
                        'F': pd.date_range('2016-01-01', periods=3,
                                           tz='America/New_York'),
                        'G': pd.Timedelta('1 hours'),
                        'H': np.void(b' ')},
                       columns=list('DCBAHGFE'))
    df2 = df1.iloc[0:0]
    df3 = meta_nonempty(df2)
    assert (df3.dtypes == df2.dtypes).all()
    assert df3['A'][0] == 'Alice'
    assert df3['B'][0] == 'foo'
    assert df3['C'][0] == 'foo'
    assert df3['D'][0] == 1.0
    assert df3['E'][0] == pd.Timestamp('1970-01-01 00:00:00')
    assert df3['F'][0] == pd.Timestamp('1970-01-01 00:00:00',
                                       tz='America/New_York')
    assert df3['G'][0] == pd.Timedelta('1 days')
    assert df3['H'][0] == 'foo'

    s = meta_nonempty(df2['A'])
    assert s.dtype == df2['A'].dtype
    assert (df3['A'] == s).all()
