def test_read_bytes_sample_delimiter(s3):
    sample, values = read_bytes(test_bucket_name + '/test/accounts.*', s3=s3,
                                sample=80, delimiter=b'\n')
    assert sample.endswith(b'\n')
    sample, values = read_bytes(test_bucket_name + '/test/accounts.1.json', s3=s3,
                                sample=80, delimiter=b'\n')
    assert sample.endswith(b'\n')
    sample, values = read_bytes(test_bucket_name + '/test/accounts.1.json', s3=s3,
                                sample=2, delimiter=b'\n')
    assert sample.endswith(b'\n')
