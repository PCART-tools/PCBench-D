def test_slice_with_integer_types():
    x = np.arange(10)
    dx = da.from_array(x, chunks=5)
    inds = np.array([0, 3, 6], dtype='u8')
    assert_eq(dx[inds], x[inds])
    assert_eq(dx[inds.astype('u4')], x[inds.astype('u4')])

    inds = np.array([0, 3, 6], dtype=np.int64)
    assert_eq(dx[inds], x[inds])
    assert_eq(dx[inds.astype('u4')], x[inds.astype('u4')])
