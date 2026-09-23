def test_ellipsis_slicing():
    assert_eq(da.ones(4, chunks=2)[...], np.ones(4))
