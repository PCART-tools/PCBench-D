def test_ravel():
    x = np.random.randint(10, size=(4, 6))

    # 2d
    for chunks in [(4, 6), (2, 6)]:
        a = da.from_array(x, chunks=chunks)
        assert_eq(x.ravel(), a.ravel())
        assert len(a.ravel().dask) == len(a.dask) + len(a.chunks[0])

    # 0d
    assert_eq(x[0, 0].ravel(), a[0, 0].ravel())

    # 1d
    a_flat = a.ravel()
    assert_eq(a_flat.ravel(), a_flat)

    # 3d
    x = np.random.randint(10, size=(2, 3, 4))
    for chunks in [4, (1, 3, 4)]:
        a = da.from_array(x, chunks=chunks)
        assert_eq(x.ravel(), a.ravel())

    assert_eq(x.flatten(), a.flatten())
    assert_eq(np.ravel(x), da.ravel(a))
