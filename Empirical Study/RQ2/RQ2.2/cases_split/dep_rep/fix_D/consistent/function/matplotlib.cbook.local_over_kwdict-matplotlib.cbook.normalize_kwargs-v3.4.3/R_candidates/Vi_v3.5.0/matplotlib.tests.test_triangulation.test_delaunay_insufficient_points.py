@pytest.mark.parametrize('x, y', [
    # Triangulation should raise a ValueError if passed less than 3 points.
    ([], []),
    ([1], [5]),
    ([1, 2], [5, 6]),
    # Triangulation should also raise a ValueError if passed duplicate points
    # such that there are less than 3 unique points.
    ([1, 2, 1], [5, 6, 5]),
    ([1, 2, 2], [5, 6, 6]),
    ([1, 1, 1, 2, 1, 2], [5, 5, 5, 6, 5, 6]),
])
def test_delaunay_insufficient_points(x, y):
    with pytest.raises(ValueError):
        mtri.Triangulation(x, y)
