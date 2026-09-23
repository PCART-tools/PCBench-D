    class BadCV():
        def split(self, X, y=None, groups=None):
            for i in range(4):
                yield np.array([0, 1, 2, 3]), np.array([4, 5, 6, 7, 8])
