def test_to_hdf5():
    h5py = pytest.importorskip('h5py')
    x = da.ones((4, 4), chunks=(2, 2))
    y = da.ones(4, chunks=2, dtype='i4')

    with tmpfile('.hdf5') as fn:
        x.to_hdf5(fn, '/x')
        with h5py.File(fn) as f:
            d = f['/x']

            assert_eq(d[:], x)
            assert d.chunks == (2, 2)

    with tmpfile('.hdf5') as fn:
        x.to_hdf5(fn, '/x', chunks=None)
        with h5py.File(fn) as f:
            d = f['/x']

            assert_eq(d[:], x)
            assert d.chunks is None

    with tmpfile('.hdf5') as fn:
        x.to_hdf5(fn, '/x', chunks=(1, 1))
        with h5py.File(fn) as f:
            d = f['/x']

            assert_eq(d[:], x)
            assert d.chunks == (1, 1)

    with tmpfile('.hdf5') as fn:
        da.to_hdf5(fn, {'/x': x, '/y': y})

        with h5py.File(fn) as f:
            assert_eq(f['/x'][:], x)
            assert f['/x'].chunks == (2, 2)
            assert_eq(f['/y'][:], y)
            assert f['/y'].chunks == (2,)
