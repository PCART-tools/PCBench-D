def test_keepdims_wrapper_no_axis():
    def summer(a, axis=None):
        return a.sum(axis=axis)

    summer_wrapped = keepdims_wrapper(summer)

    assert summer_wrapped != summer
    assert summer_wrapped == keepdims_wrapper(summer_wrapped)

    a = np.arange(24).reshape(1, 2, 3, 4)

    r = summer(a)
    rw = summer_wrapped(a, keepdims=True)
    rwf = summer_wrapped(a, keepdims=False)

    assert r.ndim == 0
    assert r.shape == tuple()
    assert r == 276

    assert rw.ndim == 4
    assert rw.shape == (1, 1, 1, 1)
    assert (rw == 276).all()

    assert rwf.ndim == 0
    assert rwf.shape == tuple()
    assert rwf == 276
