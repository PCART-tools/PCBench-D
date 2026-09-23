def test_reshape_fails_for_dask_only():
    cases = [
        ((3, 4), (4, 3), 2),
    ]
    for original_shape, new_shape, chunks in cases:
        x = np.random.randint(10, size=original_shape)
        a = from_array(x, chunks=chunks)
        assert x.reshape(new_shape).shape == new_shape
        with pytest.raises(ValueError):
            da.reshape(a, new_shape)
