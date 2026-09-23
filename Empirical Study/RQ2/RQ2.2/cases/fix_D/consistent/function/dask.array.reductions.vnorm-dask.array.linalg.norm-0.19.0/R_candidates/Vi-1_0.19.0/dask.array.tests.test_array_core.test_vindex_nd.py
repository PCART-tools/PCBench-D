def test_vindex_nd():
    x = np.arange(56).reshape((7, 8))
    d = da.from_array(x, chunks=(3, 4))

    result = d.vindex[[[0, 1], [6, 0]], [[0, 1], [0, 7]]]
    assert_eq(result, x[[[0, 1], [6, 0]], [[0, 1], [0, 7]]])

    result = d.vindex[np.arange(7)[:, None], np.arange(8)[None, :]]
    assert_eq(result, x)

    result = d.vindex[np.arange(7)[None, :], np.arange(8)[:, None]]
    assert_eq(result, x.T)
