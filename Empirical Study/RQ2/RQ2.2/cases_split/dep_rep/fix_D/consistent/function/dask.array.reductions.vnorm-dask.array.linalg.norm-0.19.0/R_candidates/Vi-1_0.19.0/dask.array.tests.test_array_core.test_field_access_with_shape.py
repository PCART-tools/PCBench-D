def test_field_access_with_shape():
    dtype = [('col1', ('f4', (3, 2))), ('col2', ('f4', 3))]
    data = np.ones((100, 50), dtype=dtype)
    x = da.from_array(data, 10)
    assert_eq(x['col1'], data['col1'])
    assert_eq(x[['col1']], data[['col1']])
    assert_eq(x['col2'], data['col2'])
    assert_eq(x[['col1', 'col2']], data[['col1', 'col2']])
