def test_warn_bad_rechunking():
    x = da.ones((20, 20), chunks=(20, 1))
    y = da.ones((20, 20), chunks=(1, 20))

    with warnings.catch_warnings(record=True) as record:
        x + y

    assert record
    assert '20' in record[0].message.args[0]
