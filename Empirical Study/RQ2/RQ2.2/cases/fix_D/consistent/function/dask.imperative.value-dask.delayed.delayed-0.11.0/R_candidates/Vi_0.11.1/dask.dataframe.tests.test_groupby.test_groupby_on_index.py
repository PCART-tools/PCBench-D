def test_groupby_on_index():
    full = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                         'b': [4, 5, 6, 3, 2, 1, 0, 0, 0]},
                        index=[0, 1, 3, 5, 6, 8, 9, 9, 9])
    d = dd.from_pandas(full, npartitions=3)

    e = d.set_index('a')
    efull = full.set_index('a')
    assert eq(d.groupby('a').b.mean(), e.groupby(e.index).b.mean())

    def func(df):
        df.loc[:, 'b'] = df.b - df.b.mean()
        return df

    assert eq(d.groupby('a').apply(func).set_index('a'),
              e.groupby(e.index).apply(func))
    assert eq(d.groupby('a').apply(func), full.groupby('a').apply(func))
    assert eq(d.groupby('a').apply(func).set_index('a'),
              full.groupby('a').apply(func).set_index('a'))
    assert eq(efull.groupby(efull.index).apply(func),
              e.groupby(e.index).apply(func))
