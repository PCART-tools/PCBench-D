    @staticmethod
    def assert_almost_equal(x, y):
        ax = np.array(x)
        ay = np.array(y)
        assert np.all(ax > 0) and np.all(ax < 1)
        assert np.all(ay > 0) and np.all(ay < 1)
        lx = -np.log(1/ax-1)
        ly = -np.log(1/ay-1)
        assert_almost_equal(lx, ly)
