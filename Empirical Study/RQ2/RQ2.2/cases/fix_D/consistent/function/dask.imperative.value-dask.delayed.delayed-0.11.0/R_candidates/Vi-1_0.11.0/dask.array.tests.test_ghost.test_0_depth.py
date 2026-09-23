def test_0_depth():
    expected = np.arange(100).reshape(10, 10)
    darr = da.from_array(expected, chunks=(5, 2))

    depth = {0: 0, 1: 0}

    reflected = ghost(darr, depth=depth, boundary='reflect')
    nearest = ghost(darr, depth=depth, boundary='nearest')
    periodic = ghost(darr, depth=depth, boundary='periodic')
    constant = ghost(darr, depth=depth, boundary=42)

    result = trim_internal(reflected, depth)
    assert_array_equal(result, expected)

    result = trim_internal(nearest, depth)
    assert_array_equal(result, expected)

    result = trim_internal(periodic, depth)
    assert_array_equal(result, expected)

    result = trim_internal(constant, depth)
    assert_array_equal(result, expected)
