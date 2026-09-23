def test__clean_inputs3():
    c = [[1, 2]]
    A_ub = np.random.rand(2, 2)
    b_ub = [[1], [2]]
    A_eq = np.random.rand(2, 2)
    b_eq = [[1], [2]]
    bounds = [(0, 1)]
    outputs = _clean_inputs(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds)
    assert_allclose(outputs[0], np.array([1, 2]))
    assert_allclose(outputs[2], np.array([1, 2]))
    assert_allclose(outputs[4], np.array([1, 2]))
    assert_(outputs[5] == [(0, 1)] * 2, "")

    assert_(outputs[0].shape == (2,), "")
    assert_(outputs[2].shape == (2,), "")
    assert_(outputs[4].shape == (2,), "")
