def test_broadcast_to():
    x = np.random.randint(10, size=(5, 1, 6))
    a = from_array(x, chunks=(3, 1, 3))

    for shape in [a.shape, (5, 0, 6), (5, 4, 6), (2, 5, 1, 6), (3, 4, 5, 4, 6)]:
        xb = chunk.broadcast_to(x, shape)
        ab = broadcast_to(a, shape)

        assert_eq(xb, ab)

        if a.shape == ab.shape:
            assert a is ab

    pytest.raises(ValueError, lambda: broadcast_to(a, (2, 1, 6)))
    pytest.raises(ValueError, lambda: broadcast_to(a, (3,)))
