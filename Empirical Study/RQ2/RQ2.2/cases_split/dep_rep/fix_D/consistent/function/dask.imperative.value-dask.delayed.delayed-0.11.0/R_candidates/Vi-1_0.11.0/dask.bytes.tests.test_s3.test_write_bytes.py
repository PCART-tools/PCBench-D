def test_write_bytes(s3):
    paths = ['s3://' + test_bucket_name + '/more/' + f for f in files]
    values = [delayed(v) for v in files.values()]
    out = core.write_bytes(values, paths, s3=s3)
    compute(*out)
    sample, values = read_bytes(test_bucket_name+'/more/test/accounts.*', s3=s3)
    results = compute(*concat(values))
    assert set(list(files.values())) == set(results)
