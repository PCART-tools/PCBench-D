def test_broadcast_arrays():
    # Calling `broadcast_arrays` with no arguments only works in NumPy 1.13.0+.
    if LooseVersion(np.__version__) >= LooseVersion("1.13.0"):
        assert np.broadcast_arrays() == da.broadcast_arrays()

    a = np.arange(4)
    d_a = da.from_array(a, chunks=tuple(s // 2 for s in a.shape))

    a_0 = np.arange(4)[None, :]
    a_1 = np.arange(4)[:, None]

    d_a_0 = d_a[None, :]
    d_a_1 = d_a[:, None]

    a_r = np.broadcast_arrays(a_0, a_1)
    d_r = da.broadcast_arrays(d_a_0, d_a_1)

    assert isinstance(d_r, list)
    assert len(a_r) == len(d_r)

    for e_a_r, e_d_r in zip(a_r, d_r):
        assert_eq(e_a_r, e_d_r)
