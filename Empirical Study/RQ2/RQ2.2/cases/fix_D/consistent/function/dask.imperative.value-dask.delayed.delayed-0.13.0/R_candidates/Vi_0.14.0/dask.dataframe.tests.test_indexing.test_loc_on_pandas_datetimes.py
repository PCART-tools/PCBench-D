def test_loc_on_pandas_datetimes():
    df = pd.DataFrame({'x': [1, 2, 3]},
                      index=list(map(pd.Timestamp, ['2014', '2015', '2016'])))
    a = dd.from_pandas(df, 2)
    a.divisions = list(map(pd.Timestamp, a.divisions))

    assert_eq(a.loc['2014': '2015'], a.loc['2014': '2015'])
