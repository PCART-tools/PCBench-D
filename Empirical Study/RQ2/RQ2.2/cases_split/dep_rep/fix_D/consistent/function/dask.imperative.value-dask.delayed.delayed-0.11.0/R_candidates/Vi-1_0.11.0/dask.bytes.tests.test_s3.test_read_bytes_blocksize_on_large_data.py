@pytest.mark.slow
def test_read_bytes_blocksize_on_large_data():
    _, L = read_bytes('s3://dask-data/nyc-taxi/2015/yellow_tripdata_2015-01.csv',
                      blocksize=None, anon=True)
    assert len(L) == 1

    _, L = read_bytes('s3://dask-data/nyc-taxi/2014/*.csv', blocksize=None, anon=True)
    assert len(L) == 12
