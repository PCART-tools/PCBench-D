def test__clean_inputs2():
    c = 1
    A_ub = [[1]]
    b_ub = 1
    A_eq = [[1]]
    b_eq = 1
    bounds = (0, 1)
    outputs = _clean_inputs(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds)
    assert_allclose(outputs[0], np.array(c))
    assert_allclose(outputs[1], np.array(A_ub))
    assert_allclose(outputs[2], np.array(b_ub))
    assert_allclose(outputs[3], np.array(A_eq))
    assert_allclose(outputs[4], np.array(b_eq))
    assert_(outputs[5] == [(0, 1)], "")

    assert_(outputs[0].shape == (1,), "")
    assert_(outputs[1].shape == (1, 1), "")
    assert_(outputs[2].shape == (1,), "")
    assert_(outputs[3].shape == (1, 1), "")
    assert_(outputs[4].shape == (1,), "")
