def test_registered_open_files(s3):
    from dask.bytes.core import open_files
    myfiles = open_files('s3://%s/test/accounts.*.json' % test_bucket_name,
                         s3=s3)
    assert len(myfiles) == len(files)
    data = compute(*[file.read() for file in myfiles])
    assert list(data) == [files[k] for k in sorted(files)]
