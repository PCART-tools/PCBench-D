def test_concatenate_fixlen_strings():
    x = np.array(['a', 'b', 'c'])
    y = np.array(['aa', 'bb', 'cc'])

    a = da.from_array(x, chunks=(2,))
    b = da.from_array(y, chunks=(2,))

    assert_eq(np.concatenate([x, y]),
              da.concatenate([a, b]))
