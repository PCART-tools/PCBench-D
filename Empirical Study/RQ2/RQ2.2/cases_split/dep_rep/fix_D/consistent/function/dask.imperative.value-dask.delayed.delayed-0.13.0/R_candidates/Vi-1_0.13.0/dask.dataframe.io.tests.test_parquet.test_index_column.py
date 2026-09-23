def test_index_column(fn):
    ddf = read_parquet(fn, columns=['myindex'], index='myindex')
    assert_eq(df[[]], ddf)
