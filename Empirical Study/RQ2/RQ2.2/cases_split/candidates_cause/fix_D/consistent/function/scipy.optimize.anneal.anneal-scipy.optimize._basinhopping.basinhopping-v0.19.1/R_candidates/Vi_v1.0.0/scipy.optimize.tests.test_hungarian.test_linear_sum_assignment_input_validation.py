def test_linear_sum_assignment_input_validation():
    assert_raises(ValueError, linear_sum_assignment, [1, 2, 3])

    C = [[1, 2, 3], [4, 5, 6]]
    assert_array_equal(linear_sum_assignment(C),
                       linear_sum_assignment(np.asarray(C)))
    assert_array_equal(linear_sum_assignment(C),
                       linear_sum_assignment(np.matrix(C)))

    I = np.identity(3)
    assert_array_equal(linear_sum_assignment(I.astype(np.bool)),
                       linear_sum_assignment(I))
    assert_raises(ValueError, linear_sum_assignment, I.astype(str))

    I[0][0] = np.nan
    assert_raises(ValueError, linear_sum_assignment, I)

    I = np.identity(3)
    I[1][1] = np.inf
    assert_raises(ValueError, linear_sum_assignment, I)
