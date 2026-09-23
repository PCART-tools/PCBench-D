def test_argwhere_str():
    x = np.array(list("Hello world"))
    d = da.from_array(x, chunks=(4,))

    x_nz = np.argwhere(x)
    d_nz = da.argwhere(d)

    assert_eq(d_nz, x_nz)
