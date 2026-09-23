def test_auto_add_index(fn):
    ddf = read_parquet(fn, columns=['x'], index='myindex')
    assert_eq(df[['x']], ddf)
