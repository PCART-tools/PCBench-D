def test_setitem_2d():
    x = np.arange(24).reshape((4, 6))
    dx = da.from_array(x.copy(), chunks=(2, 2))

    x[x > 6] = -1
    x[x % 2 == 0] = -2

    dx[dx > 6] = -1
    dx[dx % 2 == 0] = -2

    assert_eq(x, dx)
