def test_names(fn):
    assert set(read_parquet(fn).dask) == set(read_parquet(fn).dask)
    assert (set(read_parquet(fn).dask) !=
            set(read_parquet(fn, columns=['x']).dask))
    assert (set(read_parquet(fn, columns='x').dask) !=
            set(read_parquet(fn, columns=['x']).dask))
    assert (set(read_parquet(fn, columns=('x',)).dask) ==
            set(read_parquet(fn, columns=['x']).dask))
