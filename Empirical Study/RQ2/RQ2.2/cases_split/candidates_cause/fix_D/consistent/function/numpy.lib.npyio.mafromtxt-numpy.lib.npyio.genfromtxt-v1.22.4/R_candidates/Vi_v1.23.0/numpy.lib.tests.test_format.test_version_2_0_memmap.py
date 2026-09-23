def test_version_2_0_memmap(tmpdir):
    # requires more than 2 byte for header
    dt = [(("%d" % i) * 100, float) for i in range(500)]
    d = np.ones(1000, dtype=dt)
    tf1 = os.path.join(tmpdir, f'version2_01.npy')
    tf2 = os.path.join(tmpdir, f'version2_02.npy')

    # 1.0 requested but data cannot be saved this way
    assert_raises(ValueError, format.open_memmap, tf1, mode='w+', dtype=d.dtype,
                            shape=d.shape, version=(1, 0))

    ma = format.open_memmap(tf1, mode='w+', dtype=d.dtype,
                            shape=d.shape, version=(2, 0))
    ma[...] = d
    ma.flush()
    ma = format.open_memmap(tf1, mode='r')
    assert_array_equal(ma, d)

    with warnings.catch_warnings(record=True) as w:
        warnings.filterwarnings('always', '', UserWarning)
        ma = format.open_memmap(tf2, mode='w+', dtype=d.dtype,
                                shape=d.shape, version=None)
        assert_(w[0].category is UserWarning)
        ma[...] = d
        ma.flush()

    ma = format.open_memmap(tf2, mode='r')
    assert_array_equal(ma, d)
