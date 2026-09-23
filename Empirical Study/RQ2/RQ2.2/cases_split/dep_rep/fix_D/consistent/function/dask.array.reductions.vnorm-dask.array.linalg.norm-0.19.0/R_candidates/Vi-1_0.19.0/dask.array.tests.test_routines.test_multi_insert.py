def test_multi_insert():
    z = np.random.randint(10, size=(1, 2))
    c = da.from_array(z, chunks=(1, 2))
    assert_eq(np.insert(np.insert(z, [0, 1], -1, axis=0), [1], -1, axis=1),
              da.insert(da.insert(c, [0, 1], -1, axis=0), [1], -1, axis=1))
