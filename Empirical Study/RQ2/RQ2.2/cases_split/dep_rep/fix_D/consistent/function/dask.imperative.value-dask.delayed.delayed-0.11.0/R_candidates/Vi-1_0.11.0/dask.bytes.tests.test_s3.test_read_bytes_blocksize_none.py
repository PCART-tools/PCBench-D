def test_read_bytes_blocksize_none(s3):
    _, values = read_bytes(test_bucket_name+'/test/accounts.*', blocksize=None,
                           s3=s3)
    assert sum(map(len, values)) == len(files)
