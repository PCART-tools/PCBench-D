def test_registered(s3):
    from dask.bytes.core import read_bytes

    sample, values = read_bytes(
            's3://%s/test/accounts.*.json' % test_bucket_name,
            s3=s3)

    results = compute(*concat(values))
    assert set(results) == set(files.values())
