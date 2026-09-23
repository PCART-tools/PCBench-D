def test_good_bounds():
    c = [1, 2]
    outputs = _clean_inputs(c=c, bounds=None)
    assert_(outputs[5] == [(0, None)] * 2, "")

    outputs = _clean_inputs(c=c, bounds=(1, 2))
    assert_(outputs[5] == [(1, 2)] * 2, "")

    outputs = _clean_inputs(c=c, bounds=[(1, 2)])
    assert_(outputs[5] == [(1, 2)] * 2, "")

    outputs = _clean_inputs(c=c, bounds=[(1, np.inf)])
    assert_(outputs[5] == [(1, None)] * 2, "")

    outputs = _clean_inputs(c=c, bounds=[(-np.inf, 1)])
    assert_(outputs[5] == [(None, 1)] * 2, "")

    outputs = _clean_inputs(c=c, bounds=[(-np.inf, np.inf), (-np.inf, np.inf)])
    assert_(outputs[5] == [(None, None)] * 2, "")
