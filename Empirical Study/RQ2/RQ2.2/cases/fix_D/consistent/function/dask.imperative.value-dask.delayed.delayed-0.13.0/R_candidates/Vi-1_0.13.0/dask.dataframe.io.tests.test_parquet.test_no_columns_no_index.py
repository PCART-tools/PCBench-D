def test_no_columns_no_index(fn):
    ddf = read_parquet(fn, columns=[])
    assert_eq(df[[]], ddf)
