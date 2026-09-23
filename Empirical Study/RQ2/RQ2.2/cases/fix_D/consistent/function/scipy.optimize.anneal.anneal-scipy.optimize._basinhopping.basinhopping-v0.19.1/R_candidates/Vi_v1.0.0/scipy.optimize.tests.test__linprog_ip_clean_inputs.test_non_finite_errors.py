def test_non_finite_errors():
    c = [1, 2]
    A_ub = np.array([[1, 1], [2, 2]])
    b_ub = np.array([1, 1])
    A_eq = np.array([[1, 1], [2, 2]])
    b_eq = np.array([1, 1])
    bounds = [(0, 1)]
    assert_raises(
        ValueError, _clean_inputs, c=[0, None], A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    assert_raises(
        ValueError, _clean_inputs, c=[np.inf, 0], A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    assert_raises(
        ValueError, _clean_inputs, c=[0, -np.inf], A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    assert_raises(
        ValueError, _clean_inputs, c=[np.nan, 0], A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq, bounds=bounds)

    assert_raises(ValueError, _clean_inputs, c=c, A_ub=[[1, 2], [None, 1]],
                  b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    assert_raises(
        ValueError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=[
            np.inf,
            1],
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds)
    assert_raises(ValueError, _clean_inputs, c=c, A_ub=A_ub, b_ub=b_ub, A_eq=[
                  [1, 2], [1, -np.inf]], b_eq=b_eq, bounds=bounds)
    assert_raises(
        ValueError,
        _clean_inputs,
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=[
            1,
            np.nan],
        bounds=bounds)
