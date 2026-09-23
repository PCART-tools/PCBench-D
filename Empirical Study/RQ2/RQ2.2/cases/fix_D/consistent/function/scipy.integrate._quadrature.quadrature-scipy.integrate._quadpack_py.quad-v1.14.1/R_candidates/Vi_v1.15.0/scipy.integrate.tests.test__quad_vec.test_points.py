@pytest.mark.parametrize('a,b', [(0, 1), (0, np.inf), (np.inf, 0),
                                 (-np.inf, np.inf), (np.inf, -np.inf)])
def test_points(a, b):
    # Check that initial interval splitting is done according to
    # `points`, by checking that consecutive sets of 15 point (for
    # gk15) function evaluations lie between `points`

    points = (0, 0.25, 0.5, 0.75, 1.0)
    points += tuple(-x for x in points)

    quadrature_points = 15
    interval_sets = []
    count = 0

    def f(x):
        nonlocal count

        if count % quadrature_points == 0:
            interval_sets.append(set())

        count += 1
        interval_sets[-1].add(float(x))
        return 0.0

    quad_vec(f, a, b, points=points, quadrature='gk15', limit=0)

    # Check that all point sets lie in a single `points` interval
    for p in interval_sets:
        j = np.searchsorted(sorted(points), tuple(p))
        assert np.all(j == j[0])
