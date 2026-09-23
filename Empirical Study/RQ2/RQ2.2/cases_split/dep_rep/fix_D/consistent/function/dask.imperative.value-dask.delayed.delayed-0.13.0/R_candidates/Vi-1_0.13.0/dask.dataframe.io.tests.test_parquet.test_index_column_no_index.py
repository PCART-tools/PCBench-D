def test_index_column_no_index(fn):
    ddf = read_parquet(fn, columns=['myindex'])
    assert_eq(df[[]], ddf)
