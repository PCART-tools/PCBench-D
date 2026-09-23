def test_write_bytes(s3):
    paths = ['s3://' + test_bucket_name + '/more/' + f for f in files]
    values = [delayed(v) for v in files.values()]
    out = core.write_bytes(values, paths)
    compute(*out)
    sample, values = read_bytes('s3://' + test_bucket_name + '/more/test/accounts.*')
    results = compute(*concat(values))
    assert set(list(files.values())) == set(results)
