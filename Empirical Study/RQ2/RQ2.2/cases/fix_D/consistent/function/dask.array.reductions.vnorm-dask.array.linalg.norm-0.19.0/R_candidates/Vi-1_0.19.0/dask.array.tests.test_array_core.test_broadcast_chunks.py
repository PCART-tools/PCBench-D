def test_broadcast_chunks():
    assert broadcast_chunks() == ()

    assert broadcast_chunks(((2, 3),)) == ((2, 3),)

    assert broadcast_chunks(((5, 5),), ((5, 5),)) == ((5, 5),)

    a = ((10, 10, 10), (5, 5),)
    b = ((5, 5),)
    assert broadcast_chunks(a, b) == ((10, 10, 10), (5, 5),)
    assert broadcast_chunks(b, a) == ((10, 10, 10), (5, 5),)

    a = ((10, 10, 10), (5, 5),)
    b = ((1,), (5, 5),)
    assert broadcast_chunks(a, b) == ((10, 10, 10), (5, 5),)

    a = ((10, 10, 10), (5, 5),)
    b = ((3, 3,), (5, 5),)
    with pytest.raises(ValueError):
        broadcast_chunks(a, b)

    a = ((1,), (5, 5),)
    b = ((1,), (5, 5),)
    assert broadcast_chunks(a, b) == a

    a = ((1,), (np.nan, np.nan, np.nan),)
    b = ((3, 3), (1,),)
    r = broadcast_chunks(a, b)
    assert r[0] == b[0] and np.allclose(r[1], a[1], equal_nan=True)

    a = ((3, 3), (1,),)
    b = ((1,), (np.nan, np.nan, np.nan),)
    r = broadcast_chunks(a, b)
    assert r[0] == a[0] and np.allclose(r[1], b[1], equal_nan=True)

    a = ((3, 3,), (5, 5),)
    b = ((1,), (np.nan, np.nan, np.nan),)
    with pytest.raises(ValueError):
        broadcast_chunks(a, b)
