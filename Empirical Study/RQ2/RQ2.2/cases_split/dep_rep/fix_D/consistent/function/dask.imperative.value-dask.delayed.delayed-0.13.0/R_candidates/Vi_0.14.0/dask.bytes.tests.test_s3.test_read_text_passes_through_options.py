def test_read_text_passes_through_options():
    db = pytest.importorskip('dask.bag')
    with s3_context('csv', {'a.csv': b'a,b\n1,2\n3,4'}) as s3:
        df = db.read_text('s3://csv/*.csv', storage_options={'s3': s3})
        assert df.count().compute(get=get) == 3
