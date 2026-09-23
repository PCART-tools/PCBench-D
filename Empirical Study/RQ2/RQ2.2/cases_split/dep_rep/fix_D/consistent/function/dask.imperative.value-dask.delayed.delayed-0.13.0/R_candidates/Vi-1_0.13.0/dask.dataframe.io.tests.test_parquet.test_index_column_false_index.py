def test_index_column_false_index(fn):
    ddf = read_parquet(fn, columns=['myindex'], index=False)
    assert_eq(pd.DataFrame(df.index), ddf, check_index=False)
