def test_read_csv_passes_through_options():
    dd = pytest.importorskip('dask.dataframe')
    with s3_context('csv', {'a.csv': b'a,b\n1,2\n3,4'}) as s3:
        df = dd.read_csv('s3://csv/*.csv', storage_options={'s3': s3})
        assert df.a.sum().compute() == 1 + 3
