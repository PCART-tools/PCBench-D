def test_zero_slice_dtypes():
    x = da.arange(5, chunks=1)
    y = x[[]]
    assert y.dtype == x.dtype
    assert y.shape == (0,)
    assert_eq(x[[]], np.arange(5)[[]])
