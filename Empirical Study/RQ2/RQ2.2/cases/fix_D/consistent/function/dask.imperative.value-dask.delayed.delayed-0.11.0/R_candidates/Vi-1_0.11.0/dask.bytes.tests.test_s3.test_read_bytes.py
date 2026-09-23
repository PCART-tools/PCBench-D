def test_read_bytes(s3):
    sample, values = read_bytes(test_bucket_name+'/test/accounts.*', s3=s3)
    assert isinstance(sample, bytes)
    assert sample[:5] == files[sorted(files)[0]][:5]

    assert isinstance(values, (list, tuple))
    assert isinstance(values[0], (list, tuple))
    assert hasattr(values[0][0], 'dask')

    assert sum(map(len, values)) >= len(files)
    results = compute(*concat(values))
    assert set(results) == set(files.values())
