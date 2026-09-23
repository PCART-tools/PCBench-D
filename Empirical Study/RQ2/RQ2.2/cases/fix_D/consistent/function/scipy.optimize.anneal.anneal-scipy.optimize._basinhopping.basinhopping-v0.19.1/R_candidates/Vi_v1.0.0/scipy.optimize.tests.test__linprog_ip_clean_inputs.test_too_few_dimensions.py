def test_too_few_dimensions():
    bad = np.random.rand(4, 4).ravel()
    cb = np.random.rand(4)
    assert_raises(ValueError, _clean_inputs, c=cb, A_ub=bad, b_ub=cb)
    assert_raises(ValueError, _clean_inputs, c=cb, A_eq=bad, b_eq=cb)
