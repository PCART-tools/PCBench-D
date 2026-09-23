def test_point_in_path():
    # Test #1787
    verts2 = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]

    path = Path(verts2, closed=True)
    points = [(0.5, 0.5), (1.5, 0.5)]
    ret = path.contains_points(points)
    assert ret.dtype == 'bool'
    np.testing.assert_equal(ret, [True, False])
