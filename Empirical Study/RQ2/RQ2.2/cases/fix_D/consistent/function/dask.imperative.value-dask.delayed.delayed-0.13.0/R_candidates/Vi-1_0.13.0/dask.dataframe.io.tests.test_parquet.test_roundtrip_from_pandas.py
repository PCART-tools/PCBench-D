def test_roundtrip_from_pandas():
    with tmpfile() as fn:
        df = pd.DataFrame({'x': [1, 2, 3]})
        fastparquet.write(fn, df)
        ddf = dd.io.parquet.read_parquet(fn, index=False)
        assert_eq(df, ddf)
