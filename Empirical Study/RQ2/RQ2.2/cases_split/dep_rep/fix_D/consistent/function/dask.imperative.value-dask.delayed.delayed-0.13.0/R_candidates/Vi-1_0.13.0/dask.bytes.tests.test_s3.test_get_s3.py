def test_get_s3():
    s3 = DaskS3FileSystem(key='key', secret='secret')
    assert s3.key == 'key'
    assert s3.secret == 'secret'

    s3 = DaskS3FileSystem(username='key', password='secret')
    assert s3.key == 'key'
    assert s3.secret == 'secret'

    with pytest.raises(KeyError):
        DaskS3FileSystem(key='key', username='key')
    with pytest.raises(KeyError):
        DaskS3FileSystem(secret='key', password='key')
