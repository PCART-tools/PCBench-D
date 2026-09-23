def test_asarray_h5py():
    h5py = pytest.importorskip('h5py')

    with tmpfile('.hdf5') as fn:
        with h5py.File(fn) as f:
            d = f.create_dataset('/x', shape=(2, 2), dtype=float)
            x = da.asarray(d)
            assert d in x.dask.values()
            assert not any(isinstance(v, np.ndarray) for v in x.dask.values())
