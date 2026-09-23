def test_broadcast_to_array():
    x = np.random.randint(10, size=(5, 1, 6))

    for shape in [(5, 0, 6), (5, 4, 6), (2, 5, 1, 6), (3, 4, 5, 4, 6)]:
        a = np.broadcast_to(x, shape)
        d = broadcast_to(x, shape)

        assert_eq(a, d)
