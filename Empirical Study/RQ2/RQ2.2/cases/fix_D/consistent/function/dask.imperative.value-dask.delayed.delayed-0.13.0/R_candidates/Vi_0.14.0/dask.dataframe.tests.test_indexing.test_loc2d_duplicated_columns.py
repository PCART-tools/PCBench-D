def test_loc2d_duplicated_columns():
    df = pd.DataFrame(np.random.randn(20, 5),
                      index=list('abcdefghijklmnopqrst'),
                      columns=list('AABCD'))
    ddf = dd.from_pandas(df, 3)

    assert_eq(ddf.loc['a', 'A'], df.loc[['a'], 'A'])
    assert_eq(ddf.loc['a', ['A']], df.loc[['a'], ['A']])
    assert_eq(ddf.loc['j', 'B'], df.loc[['j'], 'B'])
    assert_eq(ddf.loc['j', ['B']], df.loc[['j'], ['B']])

    assert_eq(ddf.loc['a':'o', 'A'], df.loc['a':'o', 'A'])
    assert_eq(ddf.loc['a':'o', ['A']], df.loc['a':'o', ['A']])
    assert_eq(ddf.loc['j':'q', 'B'], df.loc['j':'q', 'B'])
    assert_eq(ddf.loc['j':'q', ['B']], df.loc['j':'q', ['B']])

    assert_eq(ddf.loc['a':'o', 'B':'D'], df.loc['a':'o', 'B':'D'])
    assert_eq(ddf.loc['a':'o', 'B':'D'], df.loc['a':'o', 'B':'D'])
    assert_eq(ddf.loc['j':'q', 'B':'A'], df.loc['j':'q', 'B':'A'])
    assert_eq(ddf.loc['j':'q', 'B':'A'], df.loc['j':'q', 'B':'A'])

    assert_eq(ddf.loc[ddf.B > 0, 'B'], df.loc[df.B > 0, 'B'])
    assert_eq(ddf.loc[ddf.B > 0, ['A', 'C']], df.loc[df.B > 0, ['A', 'C']])
