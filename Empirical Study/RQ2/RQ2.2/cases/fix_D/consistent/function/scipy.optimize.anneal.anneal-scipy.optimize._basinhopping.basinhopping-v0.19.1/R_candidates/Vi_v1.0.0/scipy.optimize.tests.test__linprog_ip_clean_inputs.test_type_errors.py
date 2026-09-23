def test_type_errors():
    bad = "hello"
    c = [1, 2]
    A_ub = np.array([[1, 1], [2, 2]])
    b_ub = np.array([1, 1])
    A_eq = np.array([[1, 1], [2, 2]])
    b_eq = np.array([1, 1])
    bounds = [(0, 1)]
    assert_raises(
        TypeError,
        _clean_inputs,
        c=bad,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds)
    assert_raises(
        TypeError,
        _clean_inputs,
        c=c,
        A_ub=bad,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds)
    assert_raises(
        TypeError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=bad,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds)
    assert_raises(
        TypeError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=bad,
        b_eq=b_eq,
        bounds=bounds)

    assert_raises(
        TypeError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bad)
    assert_raises(
        TypeError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds="hi")
    assert_raises(
        TypeError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=["hi"])
    assert_raises(
        TypeError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[
            ("hi")])
    assert_raises(TypeError, _clean_inputs, c=c, A_ub=A_ub,
                  b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(1, "")])
    assert_raises(TypeError, _clean_inputs, c=c, A_ub=A_ub,
                  b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(1, 2), (1, "")])
