def test_lnB():
    alpha = np.array([1, 1, 1])
    desired = .5  # e^lnB = 1/2 for [1, 1, 1]

    assert_almost_equal(np.exp(_lnB(alpha)), desired)
