def test_no_columns_yes_index(fn):
    ddf = read_parquet(fn, columns=[], index='myindex')
    assert_eq(df[[]], ddf)
