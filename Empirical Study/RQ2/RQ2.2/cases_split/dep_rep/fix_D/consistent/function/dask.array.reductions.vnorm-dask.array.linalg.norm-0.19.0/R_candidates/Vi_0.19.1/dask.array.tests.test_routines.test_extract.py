def test_extract():
    x = np.arange(25).reshape((5, 5))
    a = da.from_array(x, chunks=(2, 2))

    c1 = np.array([True, False, True, False, True])
    c2 = np.array([[True, False], [True, False]])
    c3 = np.array([True, False])
    dc1 = da.from_array(c1, chunks=3)
    dc2 = da.from_array(c2, chunks=(2, 1))
    dc3 = da.from_array(c3, chunks=2)

    for c, dc in [(c1, c1), (c2, c2), (c3, c3),
                  (c1, dc1), (c2, dc2), (c3, dc3)]:
        res = da.extract(dc, a)
        assert_eq(np.extract(c, x), res)
        if isinstance(dc, da.Array):
            assert np.isnan(res.chunks[0]).all()
