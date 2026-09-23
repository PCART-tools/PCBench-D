def test_3851():
    with warnings.catch_warnings() as record:
        Y = da.random.random((10, 10), chunks='auto')
        da.argmax(Y, axis=0).compute()

    assert not record
