def test_read_bytes_non_existing_glob(s3):
    with pytest.raises(IOError):
        read_bytes('s3://' + test_bucket_name + '/non-existing/*')
