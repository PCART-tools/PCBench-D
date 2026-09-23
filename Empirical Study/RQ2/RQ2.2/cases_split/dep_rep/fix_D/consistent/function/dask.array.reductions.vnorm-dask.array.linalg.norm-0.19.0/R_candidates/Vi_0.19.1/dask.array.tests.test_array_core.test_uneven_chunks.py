def test_uneven_chunks():
    a = Array({}, 'x', chunks=(3, 3), shape=(10, 10), dtype='f8')
    assert a.chunks == ((3, 3, 3, 1), (3, 3, 3, 1))
