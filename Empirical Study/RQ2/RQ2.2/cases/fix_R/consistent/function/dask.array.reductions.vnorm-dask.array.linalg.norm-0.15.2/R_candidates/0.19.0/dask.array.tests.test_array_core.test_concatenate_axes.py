def test_concatenate_axes():
    x = np.ones((2, 2, 2))

    assert_eq(concatenate_axes([x, x], axes=[0]),
              np.ones((4, 2, 2)))
    assert_eq(concatenate_axes([x, x, x], axes=[0]),
              np.ones((6, 2, 2)))
    assert_eq(concatenate_axes([x, x], axes=[1]),
              np.ones((2, 4, 2)))
    assert_eq(concatenate_axes([[x, x], [x, x]], axes=[0, 1]),
              np.ones((4, 4, 2)))
    assert_eq(concatenate_axes([[x, x], [x, x]], axes=[0, 2]),
              np.ones((4, 2, 4)))
    assert_eq(concatenate_axes([[x, x, x], [x, x, x]], axes=[1, 2]),
              np.ones((2, 4, 6)))

    with pytest.raises(ValueError):
        concatenate_axes([[x, x], [x, x]], axes=[0])  # not all nested lists accounted for
    with pytest.raises(ValueError):
        concatenate_axes([x, x], axes=[0, 1, 2, 3])  # too many axes
