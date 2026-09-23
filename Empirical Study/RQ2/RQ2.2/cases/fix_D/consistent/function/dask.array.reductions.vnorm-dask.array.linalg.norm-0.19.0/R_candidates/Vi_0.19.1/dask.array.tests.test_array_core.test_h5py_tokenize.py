def test_h5py_tokenize():
    h5py = pytest.importorskip('h5py')
    with tmpfile('hdf5') as fn1:
        with tmpfile('hdf5') as fn2:
            f = h5py.File(fn1)
            g = h5py.File(fn2)

            f['x'] = np.arange(10).astype(float)
            g['x'] = np.ones(10).astype(float)

            x1 = f['x']
            x2 = g['x']

            assert tokenize(x1) != tokenize(x2)
