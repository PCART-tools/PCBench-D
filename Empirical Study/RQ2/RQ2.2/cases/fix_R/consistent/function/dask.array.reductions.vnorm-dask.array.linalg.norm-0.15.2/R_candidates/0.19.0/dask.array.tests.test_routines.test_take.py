def test_take():
    x = np.arange(400).reshape((20, 20))
    a = da.from_array(x, chunks=(5, 5))

    assert_eq(np.take(x, 3, axis=0), da.take(a, 3, axis=0))
    assert_eq(np.take(x, [3, 4, 5], axis=-1), da.take(a, [3, 4, 5], axis=-1))

    with pytest.raises(ValueError):
        da.take(a, 3, axis=2)

    assert same_keys(da.take(a, [3, 4, 5], axis=-1),
                     da.take(a, [3, 4, 5], axis=-1))
