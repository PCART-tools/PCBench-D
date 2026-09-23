@pytest.mark.parametrize('aggfunc', ['mean', 'sum', 'count'])
def test_pivot_table(aggfunc):
    df = pd.DataFrame({'A': np.random.choice(list('XYZ'), size=100),
                       'B': np.random.randn(100),
                       'C': pd.Categorical(np.random.choice(list('abc'), size=100))})
    ddf = dd.from_pandas(df, 5)

    res = dd.pivot_table(ddf, index='A', columns='C', values='B',
                         aggfunc=aggfunc)
    exp = pd.pivot_table(df, index='A', columns='C', values='B',
                         aggfunc=aggfunc)
    if aggfunc == 'count':
        # dask result cannot be int64 dtype depending on divisions because of NaN
        exp = exp.astype(np.float64)

    assert_eq(res, exp)

    # method
    res = ddf.pivot_table(index='A', columns='C', values='B',
                          aggfunc=aggfunc)
    exp = df.pivot_table(index='A', columns='C', values='B',
                         aggfunc=aggfunc)
    if aggfunc == 'count':
        # dask result cannot be int64 dtype depending on divisions because of NaN
        exp = exp.astype(np.float64)
    assert_eq(res, exp)
