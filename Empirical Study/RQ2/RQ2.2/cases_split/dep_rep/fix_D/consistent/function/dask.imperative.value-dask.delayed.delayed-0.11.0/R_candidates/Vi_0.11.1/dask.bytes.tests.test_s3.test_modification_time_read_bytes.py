def test_modification_time_read_bytes():
    with s3_context('compress', files) as s3:
        _, a = read_bytes('compress/test/accounts.*', s3=s3)
        _, b = read_bytes('compress/test/accounts.*', s3=s3)

        assert [aa._key for aa in concat(a)] == [bb._key for bb in concat(b)]

    with s3_context('compress', valmap(double, files)) as s3:
        _, c = read_bytes('compress/test/accounts.*', s3=s3)

    assert [aa._key for aa in concat(a)] != [cc._key for cc in concat(c)]
