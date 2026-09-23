def test_categorical():
    with tmpdir() as tmp:
        df = pd.DataFrame({'x': ['a', 'b', 'c'] * 100},
                          dtype='category')
        ddf = dd.from_pandas(df, npartitions=3)
        to_parquet(tmp, ddf)

        ddf2 = read_parquet(tmp, categories=['x'])

        assert ddf2.x.cat.categories.tolist() == ['a', 'b', 'c']
        ddf2.loc[:1000].compute()
        df.index.name = 'index'  # defaults to 'index' in this case
        assert assert_eq(df, ddf2)
