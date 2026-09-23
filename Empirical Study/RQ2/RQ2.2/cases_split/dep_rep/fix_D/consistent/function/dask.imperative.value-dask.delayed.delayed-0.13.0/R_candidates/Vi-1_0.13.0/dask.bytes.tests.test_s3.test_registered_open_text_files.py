def test_registered_open_text_files(s3):
    myfiles = open_text_files('s3://%s/test/accounts.*.json' % test_bucket_name)
    assert len(myfiles) == len(files)
    data = []
    for file in myfiles:
        with file as f:
            data.append(f.read())
    assert list(data) == [files[k].decode() for k in sorted(files)]
