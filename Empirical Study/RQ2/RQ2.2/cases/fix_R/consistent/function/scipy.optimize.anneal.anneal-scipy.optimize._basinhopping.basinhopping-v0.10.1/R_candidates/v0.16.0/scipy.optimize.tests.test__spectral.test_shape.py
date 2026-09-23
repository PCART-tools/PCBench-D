def test_shape():
    def f(x, arg):
        return x - arg

    for dt in [float, complex]:
        x = np.zeros([2,2])
        arg = np.ones([2,2], dtype=dt)

        sol = root(f, x, args=(arg,), method='DF-SANE')
        assert_(sol.success)
        assert_equal(sol.x.shape, x.shape)
