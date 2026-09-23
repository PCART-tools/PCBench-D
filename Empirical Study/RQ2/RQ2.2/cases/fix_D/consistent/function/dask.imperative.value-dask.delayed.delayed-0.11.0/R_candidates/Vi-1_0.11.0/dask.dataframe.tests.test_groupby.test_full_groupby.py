def test_full_groupby():
    df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                       'b': [4, 5, 6, 3, 2, 1, 0, 0, 0]},
                      index=[0, 1, 3, 5, 6, 8, 9, 9, 9])
    ddf = dd.from_pandas(df, npartitions=3)

    assert raises(Exception, lambda: df.groupby('does_not_exist'))
    assert raises(Exception, lambda: df.groupby('a').does_not_exist)
    assert 'b' in dir(df.groupby('a'))

    def func(df):
        df['b'] = df.b - df.b.mean()
        return df

    assert eq(df.groupby('a').apply(func),
              ddf.groupby('a').apply(func))
