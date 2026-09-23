def test_nan_inf():
    def f_nan(x):
        return np.nan

    def f_inf(x):
        return np.inf if x < 0.1 else 1/x

    res, err, info = quad_vec(f_nan, 0, 1, full_output=True)
    assert info.status == 3

    res, err, info = quad_vec(f_inf, 0, 1, full_output=True)
    assert info.status == 3
