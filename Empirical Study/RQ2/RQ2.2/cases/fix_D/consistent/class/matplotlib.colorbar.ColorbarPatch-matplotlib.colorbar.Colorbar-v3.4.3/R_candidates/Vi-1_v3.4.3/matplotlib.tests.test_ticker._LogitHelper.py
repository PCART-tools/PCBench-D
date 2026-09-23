class _LogitHelper:
    @staticmethod
    def isclose(x, y):
        return (np.isclose(-np.log(1/x-1), -np.log(1/y-1))
                if 0 < x < 1 and 0 < y < 1 else False)

    @staticmethod
    def assert_almost_equal(x, y):
        ax = np.array(x)
        ay = np.array(y)
        assert np.all(ax > 0) and np.all(ax < 1)
        assert np.all(ay > 0) and np.all(ay < 1)
        lx = -np.log(1/ax-1)
        ly = -np.log(1/ay-1)
        assert_almost_equal(lx, ly)
