def test_local():
    with tmpdir() as tmp:
        tmp = str(tmp)
        data = pd.DataFrame({'i32': np.arange(1000, dtype=np.int32),
                             'i64': np.arange(1000, dtype=np.int64),
                             'f': np.arange(1000, dtype=np.float64),
                             'bhello': np.random.choice(['hello', 'you', 'people'], size=1000).astype("O")})
        df = dd.from_pandas(data, chunksize=500)

        df.to_parquet(tmp, write_index=False, object_encoding='utf8')

        files = os.listdir(tmp)
        assert '_metadata' in files
        assert 'part.0.parquet' in files

        df2 = read_parquet(tmp, index=False)

        assert len(df2.divisions) > 1

        out = df2.compute(get=dask.get).reset_index()

        for column in df.columns:
            assert (data[column] == out[column]).all()
