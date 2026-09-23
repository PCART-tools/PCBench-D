def test_field_access():
    x = np.array([(1, 1.0), (2, 2.0)], dtype=[('a', 'i4'), ('b', 'f4')])
    y = from_array(x, chunks=(1,))
    assert_eq(y['a'], x['a'])
    assert_eq(y[['b', 'a']], x[['b', 'a']])
    assert same_keys(y[['b', 'a']], y[['b', 'a']])
