def test_read_bytes_blocksize_none(s3):
    _, values = read_bytes('s3://' + test_bucket_name + '/test/accounts.*',
                           blocksize=None)
    assert sum(map(len, values)) == len(files)
