def test_empty_list():
    x = np.ones((5, 5, 5), dtype='i4')
    dx = da.from_array(x, chunks=2)

    assert_eq(dx[[], :3, :2], x[[], :3, :2])
    assert_eq(dx[:3, [], :2], x[:3, [], :2])
    assert_eq(dx[:3, :2, []], x[:3, :2, []])
