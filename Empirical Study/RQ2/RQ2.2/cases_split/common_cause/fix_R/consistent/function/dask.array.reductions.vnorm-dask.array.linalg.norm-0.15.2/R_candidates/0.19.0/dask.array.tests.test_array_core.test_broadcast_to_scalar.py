def test_broadcast_to_scalar():
    x = 5

    for shape in [tuple(), (0,), (2, 3), (5, 4, 6), (2, 5, 1, 6), (3, 4, 5, 4, 6)]:
        a = np.broadcast_to(x, shape)
        d = broadcast_to(x, shape)

        assert_eq(a, d)
