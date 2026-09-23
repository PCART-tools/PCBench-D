def test_meshgrid_inputcoercion():
    a = [1, 2, 3]
    b = np.array([4, 5, 6, 7])
    x, y = np.meshgrid(a, b, indexing='ij')
    z = x * y

    x_d, y_d = da.meshgrid(a, b, indexing='ij')
    z_d = x_d * y_d

    assert z_d.shape == (len(a), len(b))
    assert_eq(z, z_d)
