def test_broadcast_against_zero_shape():
    assert_eq(da.arange(1, chunks=1)[:0] + 0,
              np.arange(1)[:0] + 0)
    assert_eq(da.arange(1, chunks=1)[:0] + 0.1,
              np.arange(1)[:0] + 0.1)
    assert_eq(da.ones((5, 5), chunks=(2, 3))[:0] + 0,
              np.ones((5, 5))[:0] + 0)
    assert_eq(da.ones((5, 5), chunks=(2, 3))[:0] + 0.1,
              np.ones((5, 5))[:0] + 0.1)
    assert_eq(da.ones((5, 5), chunks=(2, 3))[:, :0] + 0,
              np.ones((5, 5))[:, :0] + 0)
    assert_eq(da.ones((5, 5), chunks=(2, 3))[:, :0] + 0.1,
              np.ones((5, 5))[:, :0] + 0.1)
