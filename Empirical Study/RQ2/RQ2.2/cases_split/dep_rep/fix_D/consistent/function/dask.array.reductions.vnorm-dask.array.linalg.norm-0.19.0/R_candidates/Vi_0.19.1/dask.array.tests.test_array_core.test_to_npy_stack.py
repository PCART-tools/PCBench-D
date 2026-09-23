def test_to_npy_stack():
    x = np.arange(5 * 10 * 10).reshape((5, 10, 10))
    d = da.from_array(x, chunks=(2, 4, 4))

    with tmpdir() as dirname:
        stackdir = os.path.join(dirname, 'test')
        da.to_npy_stack(stackdir, d, axis=0)
        assert os.path.exists(os.path.join(stackdir, '0.npy'))
        assert (np.load(os.path.join(stackdir, '1.npy')) == x[2:4]).all()

        e = da.from_npy_stack(stackdir)
        assert_eq(d, e)
