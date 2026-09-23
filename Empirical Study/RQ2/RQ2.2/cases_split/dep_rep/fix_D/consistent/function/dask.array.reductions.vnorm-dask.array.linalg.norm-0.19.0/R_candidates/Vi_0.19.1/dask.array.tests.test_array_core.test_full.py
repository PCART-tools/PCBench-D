def test_full():
    d = da.full((3, 4), 2, chunks=((2, 1), (2, 2)))
    assert d.chunks == ((2, 1), (2, 2))
    assert_eq(d, np.full((3, 4), 2))
