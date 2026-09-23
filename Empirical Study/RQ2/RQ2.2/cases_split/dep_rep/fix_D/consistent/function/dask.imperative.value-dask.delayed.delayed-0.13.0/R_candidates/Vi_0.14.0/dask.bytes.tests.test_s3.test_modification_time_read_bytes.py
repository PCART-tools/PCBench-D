def test_modification_time_read_bytes():
    with s3_context('compress', files):
        _, a = read_bytes('s3://compress/test/accounts.*')
        _, b = read_bytes('s3://compress/test/accounts.*')

        assert [aa._key for aa in concat(a)] == [bb._key for bb in concat(b)]

    with s3_context('compress', valmap(double, files)):
        _, c = read_bytes('s3://compress/test/accounts.*')

    assert [aa._key for aa in concat(a)] != [cc._key for cc in concat(c)]
