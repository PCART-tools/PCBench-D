def test_insert():
    x = np.random.randint(10, size=(10, 10))
    a = da.from_array(x, chunks=(5, 5))
    y = np.random.randint(10, size=(5, 10))
    b = da.from_array(y, chunks=(4, 4))

    assert_eq(np.insert(x, 0, -1, axis=0), da.insert(a, 0, -1, axis=0))
    assert_eq(np.insert(x, 3, -1, axis=-1), da.insert(a, 3, -1, axis=-1))
    assert_eq(np.insert(x, 5, -1, axis=1), da.insert(a, 5, -1, axis=1))
    assert_eq(np.insert(x, -1, -1, axis=-2), da.insert(a, -1, -1, axis=-2))
    assert_eq(np.insert(x, [2, 3, 3], -1, axis=1),
              da.insert(a, [2, 3, 3], -1, axis=1))
    assert_eq(np.insert(x, [2, 3, 8, 8, -2, -2], -1, axis=0),
              da.insert(a, [2, 3, 8, 8, -2, -2], -1, axis=0))
    assert_eq(np.insert(x, slice(1, 4), -1, axis=1),
              da.insert(a, slice(1, 4), -1, axis=1))
    assert_eq(np.insert(x, [2] * 3 + [5] * 2, y, axis=0),
              da.insert(a, [2] * 3 + [5] * 2, b, axis=0))
    assert_eq(np.insert(x, 0, y[0], axis=1),
              da.insert(a, 0, b[0], axis=1))

    assert same_keys(da.insert(a, [2, 3, 8, 8, -2, -2], -1, axis=0),
                     da.insert(a, [2, 3, 8, 8, -2, -2], -1, axis=0))

    with pytest.raises(NotImplementedError):
        da.insert(a, [4, 2], -1, axis=0)

    with pytest.raises(AxisError):
        da.insert(a, [3], -1, axis=2)

    with pytest.raises(AxisError):
        da.insert(a, [3], -1, axis=-3)
