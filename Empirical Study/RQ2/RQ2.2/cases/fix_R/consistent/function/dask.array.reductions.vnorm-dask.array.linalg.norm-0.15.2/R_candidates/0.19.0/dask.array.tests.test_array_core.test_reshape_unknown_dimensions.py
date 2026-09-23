def test_reshape_unknown_dimensions():
    for original_shape in [(24,), (2, 12), (2, 3, 4)]:
        for new_shape in [(-1,), (2, -1), (-1, 3, 4)]:
            x = np.random.randint(10, size=original_shape)
            a = from_array(x, 24)
            assert_eq(x.reshape(new_shape), a.reshape(new_shape))

    pytest.raises(ValueError, lambda: da.reshape(a, (-1, -1)))
