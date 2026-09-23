def test_None_overlap_int():
    a, b, c, d = (0, slice(None, 2, None), None, Ellipsis)
    shape = (2,3,5,7,11)
    x = np.arange(np.prod(shape)).reshape(shape)
    y = da.core.asarray(x)

    xx = x[a, b, c, d]
    yy = y[a, b, c, d]
    assert_eq(xx, yy)
