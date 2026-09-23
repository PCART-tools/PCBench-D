def test_vindex_basic():
    x = np.arange(56).reshape((7, 8))
    d = da.from_array(x, chunks=(3, 4))

    # cases where basic and advanced indexing coincide
    result = d.vindex[0]
    assert_eq(result, x[0])

    result = d.vindex[0, 1]
    assert_eq(result, x[0, 1])

    result = d.vindex[[0, 1], ::-1]  # slices last
    assert_eq(result, x[:2, ::-1])
