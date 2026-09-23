def test_trim_internal():
    d = da.ones((40, 60), chunks=(10, 10))
    e = trim_internal(d, axes={0: 1, 1: 2})

    assert e.chunks == ((8, 8, 8, 8), (6, 6, 6, 6, 6, 6))
