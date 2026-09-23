def test_loc2d_with_unknown_divisions():
    df = pd.DataFrame(np.random.randn(20, 5),
                      index=list('abcdefghijklmnopqrst'),
                      columns=list('ABCDE'))
    ddf = dd.from_pandas(df, 3)

    ddf.divisions = (None, ) * len(ddf.divisions)
    assert ddf.known_divisions is False

    assert_eq(ddf.loc['a', 'A'], df.loc[['a'], 'A'])
    assert_eq(ddf.loc['a', ['A']], df.loc[['a'], ['A']])
    assert_eq(ddf.loc['a':'o', 'A'], df.loc['a':'o', 'A'])
    assert_eq(ddf.loc['a':'o', ['A']], df.loc['a':'o', ['A']])
