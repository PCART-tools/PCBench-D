def test_files(s3):
    myfiles = open_files(test_bucket_name+'/test/accounts.*', s3=s3)
    assert len(myfiles) == len(files)
    data = compute(*[file.read() for file in myfiles])
    assert list(data) == [files[k] for k in sorted(files)]
