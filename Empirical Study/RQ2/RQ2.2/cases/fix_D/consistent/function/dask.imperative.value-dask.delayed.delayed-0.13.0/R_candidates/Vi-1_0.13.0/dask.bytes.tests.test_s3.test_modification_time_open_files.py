@pytest.mark.skip()
def test_modification_time_open_files():
    with s3_context('compress', files):
        a = open_files('s3://compress/test/accounts.*')
        b = open_files('s3://compress/test/accounts.*')

        assert [aa._key for aa in a] == [bb._key for bb in b]

    with s3_context('compress', valmap(double, files)):
        c = open_files('s3://compress/test/accounts.*')

    assert [aa._key for aa in a] != [cc._key for cc in c]
