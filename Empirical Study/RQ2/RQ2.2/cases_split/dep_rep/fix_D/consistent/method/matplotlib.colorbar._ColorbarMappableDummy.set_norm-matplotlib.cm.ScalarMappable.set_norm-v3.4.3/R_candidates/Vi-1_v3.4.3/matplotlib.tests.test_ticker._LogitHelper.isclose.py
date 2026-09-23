    @staticmethod
    def isclose(x, y):
        return (np.isclose(-np.log(1/x-1), -np.log(1/y-1))
                if 0 < x < 1 and 0 < y < 1 else False)
