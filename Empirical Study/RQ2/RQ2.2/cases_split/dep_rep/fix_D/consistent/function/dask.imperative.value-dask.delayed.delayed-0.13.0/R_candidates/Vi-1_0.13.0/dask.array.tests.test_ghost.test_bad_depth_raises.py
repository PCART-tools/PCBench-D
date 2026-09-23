def test_bad_depth_raises():
    expected = np.arange(144).reshape(12, 12)
    darr = da.from_array(expected, chunks=(5, 5))

    depth = {0: 4, 1: 2}

    pytest.raises(ValueError, ghost, darr, depth=depth, boundary=1)
