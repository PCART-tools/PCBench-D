def test_h5py_newaxis():
    h5py = pytest.importorskip('h5py')

    with tmpfile('h5') as fn:
        with h5py.File(fn) as f:
            x = f.create_dataset('/x', shape=(10, 10), dtype='f8')
            d = da.from_array(x, chunks=(5, 5))
            assert d[None, :, :].compute(scheduler='sync').shape == (1, 10, 10)
            assert d[:, None, :].compute(scheduler='sync').shape == (10, 1, 10)
            assert d[:, :, None].compute(scheduler='sync').shape == (10, 10, 1)
            assert same_keys(d[:, :, None], d[:, :, None])
