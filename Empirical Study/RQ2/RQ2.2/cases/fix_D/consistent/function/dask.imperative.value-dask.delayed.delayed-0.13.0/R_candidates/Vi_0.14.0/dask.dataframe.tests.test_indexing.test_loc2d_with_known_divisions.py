def test_loc2d_with_known_divisions():
    df = pd.DataFrame(np.random.randn(20, 5),
                      index=list('abcdefghijklmnopqrst'),
                      columns=list('ABCDE'))
    ddf = dd.from_pandas(df, 3)

    assert_eq(ddf.loc['a', 'A'], df.loc[['a'], 'A'])
    assert_eq(ddf.loc['a', ['A']], df.loc[['a'], ['A']])
    assert_eq(ddf.loc['a':'o', 'A'], df.loc['a':'o', 'A'])
    assert_eq(ddf.loc['a':'o', ['A']], df.loc['a':'o', ['A']])
    assert_eq(ddf.loc[['n'], ['A']], df.loc[['n'], ['A']])
    assert_eq(ddf.loc[['a', 'c', 'n'], ['A']], df.loc[['a', 'c', 'n'], ['A']])
    assert_eq(ddf.loc[['t', 'b'], ['A']], df.loc[['t', 'b'], ['A']])
    assert_eq(ddf.loc[['r', 'r', 'c', 'g', 'h'], ['A']],
              df.loc[['r', 'r', 'c', 'g', 'h'], ['A']])
