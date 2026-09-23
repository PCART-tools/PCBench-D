def test_boxcox_basic():
    x = np.array([0.5, 1, 2, 4])

    # lambda = 0  =>  y = log(x)
    y = boxcox(x, 0)
    yield assert_almost_equal, y, np.log(x)

    # lambda = 1  =>  y = x - 1
    y = boxcox(x, 1)
    yield assert_almost_equal, y, x - 1

    # lambda = 2  =>  y = 0.5*(x**2 - 1)
    y = boxcox(x, 2)
    yield assert_almost_equal, y, 0.5*(x**2 - 1)

    # x = 0 and lambda > 0  =>  y = -1 / lambda
    lam = np.array([0.5, 1, 2])
    y = boxcox(0, lam)
    yield assert_almost_equal, y, -1.0 / lam
