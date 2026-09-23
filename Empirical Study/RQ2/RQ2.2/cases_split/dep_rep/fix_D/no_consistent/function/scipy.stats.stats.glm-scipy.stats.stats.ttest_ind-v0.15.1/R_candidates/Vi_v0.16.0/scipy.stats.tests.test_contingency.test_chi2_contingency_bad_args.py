def test_chi2_contingency_bad_args():
    # Test that "bad" inputs raise a ValueError.

    # Negative value in the array of observed frequencies.
    obs = np.array([[-1, 10], [1, 2]])
    assert_raises(ValueError, chi2_contingency, obs)

    # The zeros in this will result in zeros in the array
    # of expected frequencies.
    obs = np.array([[0, 1], [0, 1]])
    assert_raises(ValueError, chi2_contingency, obs)

    # A degenerate case: `observed` has size 0.
    obs = np.empty((0, 8))
    assert_raises(ValueError, chi2_contingency, obs)
