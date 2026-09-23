def test_registered_open_text_files(s3):
    from dask.bytes.core import open_text_files
    myfiles = open_text_files(
            's3://%s/test/accounts.*.json' % test_bucket_name,
            s3=s3)
    assert len(myfiles) == len(files)
    data = compute(*[file.read() for file in myfiles])
    assert list(data) == [files[k].decode() for k in sorted(files)]
