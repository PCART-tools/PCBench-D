def test_index(fn):
    ddf = read_parquet(fn)
    assert_eq(df, ddf)
