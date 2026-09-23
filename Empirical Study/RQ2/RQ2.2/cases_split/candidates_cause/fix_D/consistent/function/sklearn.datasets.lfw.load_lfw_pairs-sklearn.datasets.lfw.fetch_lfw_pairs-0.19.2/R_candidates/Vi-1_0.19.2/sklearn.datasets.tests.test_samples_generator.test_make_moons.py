def test_make_moons():
    X, y = make_moons(3, shuffle=False)
    for x, label in zip(X, y):
        center = [0.0, 0.0] if label == 0 else [1.0, 0.5]
        dist_sqr = ((x - center) ** 2).sum()
        assert_almost_equal(dist_sqr, 1.0,
                            err_msg="Point is not on expected unit circle")
