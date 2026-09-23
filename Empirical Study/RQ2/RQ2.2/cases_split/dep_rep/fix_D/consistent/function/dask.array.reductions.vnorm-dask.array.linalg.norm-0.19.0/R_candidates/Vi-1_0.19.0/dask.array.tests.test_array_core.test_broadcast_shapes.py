def test_broadcast_shapes():
    assert () == broadcast_shapes()
    assert (2, 5) == broadcast_shapes((2, 5))
    assert (0, 5) == broadcast_shapes((0, 1), (1, 5))
    assert np.allclose(
        (2, np.nan), broadcast_shapes((1, np.nan), (2, 1)), equal_nan=True
    )
    assert np.allclose(
        (2, np.nan), broadcast_shapes((2, 1), (1, np.nan)), equal_nan=True
    )
    assert (3, 4, 5) == broadcast_shapes((3, 4, 5), (4, 1), ())
    assert (3, 4) == broadcast_shapes((3, 1), (1, 4), (4,))
    assert (5, 6, 7, 3, 4) == broadcast_shapes((3, 1), (), (5, 6, 7, 1, 4))
    pytest.raises(ValueError, lambda: broadcast_shapes((3,), (3, 4)))
    pytest.raises(ValueError, lambda: broadcast_shapes((2, 3), (2, 3, 1)))
    pytest.raises(ValueError, lambda: broadcast_shapes((2, 3), (1, np.nan)))
