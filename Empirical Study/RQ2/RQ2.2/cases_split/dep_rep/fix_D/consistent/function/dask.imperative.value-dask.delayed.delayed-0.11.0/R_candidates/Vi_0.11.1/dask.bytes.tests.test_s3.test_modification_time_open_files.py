def test_modification_time_open_files():
    with s3_context('compress', files) as s3:
        a = open_files('compress/test/accounts.*', s3=s3)
        b = open_files('compress/test/accounts.*', s3=s3)

        assert [aa._key for aa in a] == [bb._key for bb in b]

    with s3_context('compress', valmap(double, files)) as s3:
        c = open_files('compress/test/accounts.*', s3=s3)

    assert [aa._key for aa in a] != [cc._key for cc in c]
