def test_compress():
    x = np.arange(25).reshape((5, 5))
    a = da.from_array(x, chunks=(2, 2))

    c1 = np.array([True, False, True, False, True])
    c2 = np.array([True, False])
    c3 = [True, False]
    dc1 = da.from_array(c1, chunks=3)
    dc2 = da.from_array(c2, chunks=2)

    for c, dc in [(c1, c1), (c2, c2), (c3, c3),
                  (c1, dc1), (c2, dc2), (c3, dc2)]:
        for axis in [None, 0, 1]:
            res = da.compress(dc, a, axis=axis)
            assert_eq(np.compress(c, x, axis=axis), res)
            if isinstance(dc, da.Array):
                axis = axis or 0
                assert np.isnan(res.chunks[axis]).all()

    with pytest.raises(ValueError):
        da.compress([True, False], a, axis=100)

    with pytest.raises(ValueError):
        da.compress([[True], [False]], a, axis=100)
