def test_registered_open_files(s3):
    myfiles = open_files('s3://%s/test/accounts.*.json' % test_bucket_name)
    assert len(myfiles) == len(files)
    data = []
    for file in myfiles:
        with file as f:
            data.append(f.read())
    assert list(data) == [files[k] for k in sorted(files)]
