def test_broadcast_to_chunks():
    x = np.random.randint(10, size=(5, 1, 6))
    a = from_array(x, chunks=(3, 1, 3))

    for shape, chunks, expected_chunks in [
            ((5, 3, 6), (3, -1, 3), ((3, 2), (3,), (3, 3))),
            ((5, 3, 6), (3, 1, 3), ((3, 2), (1, 1, 1,), (3, 3))),
            ((2, 5, 3, 6), (1, 3, 1, 3), ((1, 1), (3, 2), (1, 1, 1,), (3, 3)))]:
        xb = chunk.broadcast_to(x, shape)
        ab = broadcast_to(a, shape, chunks=chunks)
        assert_eq(xb, ab)
        assert ab.chunks == expected_chunks

    with pytest.raises(ValueError):
        broadcast_to(a, a.shape, chunks=((2, 3), (1,), (3, 3)))
    with pytest.raises(ValueError):
        broadcast_to(a, a.shape, chunks=((3, 2), (3,), (3, 3)))
    with pytest.raises(ValueError):
        broadcast_to(a, (5, 2, 6), chunks=((3, 2), (3,), (3, 3)))
