def test_some_0_depth():
    expected = np.arange(100).reshape(10, 10)
    darr = da.from_array(expected, chunks=(5, 5))

    depth = {0: 4, 1: 0}

    reflected = overlap(darr, depth=depth, boundary='reflect')
    nearest = overlap(darr, depth=depth, boundary='nearest')
    periodic = overlap(darr, depth=depth, boundary='periodic')
    constant = overlap(darr, depth=depth, boundary=42)

    result = trim_internal(reflected, depth)
    assert_array_equal(result, expected)

    result = trim_internal(nearest, depth)
    assert_array_equal(result, expected)

    result = trim_internal(periodic, depth)
    assert_array_equal(result, expected)

    result = trim_internal(constant, depth)
    assert_array_equal(result, expected)
