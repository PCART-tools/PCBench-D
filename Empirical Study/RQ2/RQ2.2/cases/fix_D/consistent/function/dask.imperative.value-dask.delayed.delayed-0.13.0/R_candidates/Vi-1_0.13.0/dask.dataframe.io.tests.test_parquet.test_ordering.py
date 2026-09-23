def test_ordering():
    with tmpdir() as tmp:
        tmp = str(tmp)
        df = pd.DataFrame({'a': [1, 2, 3],
                           'b': [10, 20, 30],
                           'c': [100, 200, 300]},
                          index=pd.Index([-1, -2, -3], name='myindex'),
                          columns=['c', 'a', 'b'])
        ddf = dd.from_pandas(df, npartitions=2)
        to_parquet(tmp, ddf)

        pf = fastparquet.ParquetFile(tmp)
        assert pf.columns == ['myindex', 'c', 'a', 'b']

        ddf2 = read_parquet(tmp, index='myindex')
        assert_eq(ddf, ddf2)
