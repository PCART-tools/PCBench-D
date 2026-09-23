def test_vindex_negative():
    x = np.arange(10)
    d = da.from_array(x, chunks=(5, 5))

    result = d.vindex[np.array([0, -1])]
    assert_eq(result, x[np.array([0, -1])])
