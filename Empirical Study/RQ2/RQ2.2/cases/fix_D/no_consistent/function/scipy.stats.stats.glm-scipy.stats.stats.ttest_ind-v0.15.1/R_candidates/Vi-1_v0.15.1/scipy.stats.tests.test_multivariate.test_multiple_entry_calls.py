def test_multiple_entry_calls():
    # Test that calls with multiple x vectors as matrix work

    np.random.seed(2846)

    n = np.random.randint(1, 32)
    alpha = np.random.uniform(10e-10, 100, n)
    d = dirichlet(alpha)

    num_tests = 10
    num_multiple = 5
    xm = None
    for i in range(num_tests):
        for m in range(num_multiple):
            x = np.random.uniform(10e-10, 100, n)
            x /= np.sum(x)
            if xm is not None:
                xm = np.vstack((xm, x))
            else:
                xm = x
        rm = d.pdf(xm.T)
        rs = None
        for xs in xm:
            r = d.pdf(xs)
            if rs is not None:
                rs = np.append(rs, r)
            else:
                rs = r
        assert_array_almost_equal(rm, rs)
