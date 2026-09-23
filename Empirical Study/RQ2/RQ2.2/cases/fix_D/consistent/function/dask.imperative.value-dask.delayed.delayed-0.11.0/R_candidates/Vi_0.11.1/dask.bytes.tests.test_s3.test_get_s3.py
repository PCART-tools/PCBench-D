def test_get_s3():
    s3 = _get_s3(key='key', secret='secret')
    assert s3.key == 'key'
    assert s3.secret == 'secret'

    s3 = _get_s3(username='key', password='secret')
    assert s3.key == 'key'
    assert s3.secret == 'secret'

    with pytest.raises(KeyError):
        _get_s3(key='key', username='key')
    with pytest.raises(KeyError):
        _get_s3(secret='key', password='key')
