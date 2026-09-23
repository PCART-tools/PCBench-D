def test_files(s3):
    myfiles = open_files('s3://' + test_bucket_name + '/test/accounts.*')
    assert len(myfiles) == len(files)
    for lazy_file, path in zip(myfiles, sorted(files)):
        with lazy_file as f:
            data = f.read()
            assert data == files[path]
