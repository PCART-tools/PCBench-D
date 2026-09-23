def test_registered(s3):
    sample, values = read_bytes('s3://%s/test/accounts.*.json' % test_bucket_name)

    results = compute(*concat(values))
    assert set(results) == set(files.values())
