def test_loc_with_series_different_partition():
    df = pd.DataFrame(np.random.randn(20, 5),
                      index=list('abcdefghijklmnopqrst'),
                      columns=list('ABCDE'))
    ddf = dd.from_pandas(df, 3)

    assert_eq(ddf.loc[ddf.A > 0], df.loc[df.A > 0])
    assert_eq(ddf.loc[(ddf.A > 0).repartition(['a', 'g', 'k', 'o', 't'])],
              df.loc[df.A > 0])
