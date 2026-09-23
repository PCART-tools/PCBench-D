def test_argwhere_obj():
    x = np.random.randint(10, size=(15, 16)).astype(object)
    d = da.from_array(x, chunks=(4, 5))

    x_nz = np.argwhere(x)
    d_nz = da.argwhere(d)

    assert_eq(d_nz, x_nz)
