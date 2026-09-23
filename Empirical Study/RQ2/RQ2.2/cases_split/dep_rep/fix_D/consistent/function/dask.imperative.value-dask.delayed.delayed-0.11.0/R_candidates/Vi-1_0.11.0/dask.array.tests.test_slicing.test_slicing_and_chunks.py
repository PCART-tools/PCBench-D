def test_slicing_and_chunks():
    o = da.ones((24, 16), chunks=((4, 8, 8, 4), (2, 6, 6, 2)))
    t = o[4:-4, 2:-2]
    assert t.chunks == ((8, 8), (6, 6))
