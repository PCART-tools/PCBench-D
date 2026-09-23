def test_margins():
    a = np.array([1])
    m = margins(a)
    assert_equal(len(m), 1)
    m0 = m[0]
    assert_array_equal(m0, np.array([1]))

    a = np.array([[1]])
    m0, m1 = margins(a)
    expected0 = np.array([[1]])
    expected1 = np.array([[1]])
    assert_array_equal(m0, expected0)
    assert_array_equal(m1, expected1)

    a = np.arange(12).reshape(2, 6)
    m0, m1 = margins(a)
    expected0 = np.array([[15], [51]])
    expected1 = np.array([[6, 8, 10, 12, 14, 16]])
    assert_array_equal(m0, expected0)
    assert_array_equal(m1, expected1)

    a = np.arange(24).reshape(2, 3, 4)
    m0, m1, m2 = margins(a)
    expected0 = np.array([[[66]], [[210]]])
    expected1 = np.array([[[60], [92], [124]]])
    expected2 = np.array([[[60, 66, 72, 78]]])
    assert_array_equal(m0, expected0)
    assert_array_equal(m1, expected1)
    assert_array_equal(m2, expected2)
