def test_read_bytes_sample_delimiter(s3):
    sample, values = read_bytes('s3://' + test_bucket_name + '/test/accounts.*',
                                sample=80, delimiter=b'\n')
    assert sample.endswith(b'\n')
    sample, values = read_bytes('s3://' + test_bucket_name + '/test/accounts.1.json',
                                sample=80, delimiter=b'\n')
    assert sample.endswith(b'\n')
    sample, values = read_bytes('s3://' + test_bucket_name + '/test/accounts.1.json',
                                sample=2, delimiter=b'\n')
    assert sample.endswith(b'\n')
