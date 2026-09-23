def test_parquet_wstoragepars(s3):
    dd = pytest.importorskip('dask.dataframe')
    pytest.importorskip('fastparquet')
    from dask.dataframe.io.parquet import to_parquet, read_parquet

    import pandas as pd
    import numpy as np

    url = 's3://%s/test.parquet' % test_bucket_name

    data = pd.DataFrame({'i32': np.array([0, 5, 2, 5])})
    df = dd.from_pandas(data, chunksize=500)
    to_parquet(url, df, write_index=False)

    read_parquet(url, storage_options={'default_fill_cache': False})
    assert s3.current().default_fill_cache is False
    read_parquet(url, storage_options={'default_fill_cache': True})
    assert s3.current().default_fill_cache is True

    read_parquet(url, storage_options={'default_block_size': 2**20})
    assert s3.current().default_block_size == 2**20
    with s3.current().open(url + '/_metadata') as f:
        assert f.blocksize == 2**20
