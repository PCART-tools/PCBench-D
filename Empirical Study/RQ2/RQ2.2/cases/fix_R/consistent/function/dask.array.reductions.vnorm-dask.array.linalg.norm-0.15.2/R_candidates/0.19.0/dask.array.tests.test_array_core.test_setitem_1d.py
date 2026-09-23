def test_setitem_1d():
    x = np.arange(10)
    dx = da.from_array(x.copy(), chunks=(5,))

    x[x > 6] = -1
    x[x % 2 == 0] = -2

    dx[dx > 6] = -1
    dx[dx % 2 == 0] = -2

    assert_eq(x, dx)
