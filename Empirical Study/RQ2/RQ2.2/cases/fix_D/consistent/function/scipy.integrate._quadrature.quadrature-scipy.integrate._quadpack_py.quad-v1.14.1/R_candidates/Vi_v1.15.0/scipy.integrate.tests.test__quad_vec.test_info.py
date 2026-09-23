def test_info():
    def f(x):
        return np.ones((3, 2, 1))

    res, err, info = quad_vec(f, 0, 1, norm='max', full_output=True)

    assert info.success is True
    assert info.status == 0
    assert info.message == 'Target precision reached.'
    assert info.neval > 0
    assert info.intervals.shape[1] == 2
    assert info.integrals.shape == (info.intervals.shape[0], 3, 2, 1)
    assert info.errors.shape == (info.intervals.shape[0],)
