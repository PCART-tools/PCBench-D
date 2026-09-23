def test_masked_array():
    x = np.random.random((10, 10)).astype('f4')
    dx = da.from_array(x, chunks=(3, 4))
    f1 = da.from_array(np.array(1), chunks=())

    fill_values = [(None, None), (0.5, 0.5), (1, f1)]
    for data, (df, f) in product([x, dx], fill_values):
        assert_eq(da.ma.masked_array(data, fill_value=df),
                  np.ma.masked_array(x, fill_value=f))
        assert_eq(da.ma.masked_array(data, mask=data > 0.4, fill_value=df),
                  np.ma.masked_array(x, mask=x > 0.4, fill_value=f))
        assert_eq(da.ma.masked_array(data, mask=data > 0.4, fill_value=df),
                  np.ma.masked_array(x, mask=x > 0.4, fill_value=f))
        assert_eq(da.ma.masked_array(data, fill_value=df, dtype='f8'),
                  np.ma.masked_array(x, fill_value=f, dtype='f8'))

    with pytest.raises(ValueError):
        da.ma.masked_array(dx, fill_value=dx)

    with pytest.raises(np.ma.MaskError):
        da.ma.masked_array(dx, mask=dx[:3, :3])
