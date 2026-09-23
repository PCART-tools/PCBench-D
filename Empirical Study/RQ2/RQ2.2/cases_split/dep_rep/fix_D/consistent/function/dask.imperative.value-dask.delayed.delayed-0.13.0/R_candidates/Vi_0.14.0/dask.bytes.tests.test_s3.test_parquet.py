def test_parquet(s3):
    dd = pytest.importorskip('dask.dataframe')
    pytest.importorskip('fastparquet')
    from dask.dataframe.io.parquet import to_parquet, read_parquet

    import pandas as pd
    import numpy as np

    url = 's3://%s/test.parquet' % test_bucket_name

    data = pd.DataFrame({'i32': np.arange(1000, dtype=np.int32),
                         'i64': np.arange(1000, dtype=np.int64),
                         'f': np.arange(1000, dtype=np.float64),
                         'bhello': np.random.choice(
                             ['hello', 'you', 'people'],
                             size=1000).astype("O")},
                        index=pd.Index(np.arange(1000), name='foo'))
    df = dd.from_pandas(data, chunksize=500)
    to_parquet(url, df, object_encoding='utf8')

    files = [f.split('/')[-1] for f in s3.ls(url)]
    assert '_metadata' in files
    assert 'part.0.parquet' in files

    df2 = read_parquet(url, index='foo')
    assert len(df2.divisions) > 1

    pd.util.testing.assert_frame_equal(data, df2.compute())
