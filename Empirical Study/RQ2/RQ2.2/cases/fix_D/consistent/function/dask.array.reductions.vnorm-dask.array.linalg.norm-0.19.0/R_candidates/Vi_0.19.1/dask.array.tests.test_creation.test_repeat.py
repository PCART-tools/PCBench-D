def test_repeat():
    x = np.random.random((10, 11, 13))
    d = da.from_array(x, chunks=(4, 5, 3))

    repeats = [1, 2, 5]
    axes = [-3, -2, -1, 0, 1, 2]

    for r in repeats:
        for a in axes:
            assert_eq(x.repeat(r, axis=a), d.repeat(r, axis=a))

    assert_eq(d.repeat(2, 0), da.repeat(d, 2, 0))

    with pytest.raises(NotImplementedError):
        da.repeat(d, np.arange(10))

    with pytest.raises(NotImplementedError):
        da.repeat(d, 2, None)

    with pytest.raises(NotImplementedError):
        da.repeat(d, 2)

    for invalid_axis in [3, -4]:
        with pytest.raises(ValueError):
            da.repeat(d, 2, axis=invalid_axis)

    x = np.arange(5)
    d = da.arange(5, chunks=(2,))

    assert_eq(x.repeat(3), d.repeat(3))

    for r in [1, 2, 3, 4]:
        assert all(concat(d.repeat(r).chunks))
