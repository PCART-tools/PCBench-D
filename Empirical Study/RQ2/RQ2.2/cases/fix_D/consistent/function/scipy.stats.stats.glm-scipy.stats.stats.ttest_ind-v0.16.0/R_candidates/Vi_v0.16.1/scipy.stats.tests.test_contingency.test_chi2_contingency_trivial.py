def test_chi2_contingency_trivial():
    # Some very simple tests for chi2_contingency.

    # A trivial case
    obs = np.array([[1, 2], [1, 2]])
    chi2, p, dof, expected = chi2_contingency(obs, correction=False)
    assert_equal(chi2, 0.0)
    assert_equal(p, 1.0)
    assert_equal(dof, 1)
    assert_array_equal(obs, expected)

    # A *really* trivial case: 1-D data.
    obs = np.array([1, 2, 3])
    chi2, p, dof, expected = chi2_contingency(obs, correction=False)
    assert_equal(chi2, 0.0)
    assert_equal(p, 1.0)
    assert_equal(dof, 0)
    assert_array_equal(obs, expected)
