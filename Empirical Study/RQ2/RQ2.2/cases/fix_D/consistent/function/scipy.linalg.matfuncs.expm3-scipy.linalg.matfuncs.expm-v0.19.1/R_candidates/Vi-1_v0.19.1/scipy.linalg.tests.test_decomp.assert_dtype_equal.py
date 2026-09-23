def assert_dtype_equal(act, des):
    if isinstance(act, ndarray):
        act = act.dtype
    else:
        act = dtype(act)

    if isinstance(des, ndarray):
        des = des.dtype
    else:
        des = dtype(des)

    assert_(act == des, 'dtype mismatch: "%s" (should be "%s") ' % (act, des))
