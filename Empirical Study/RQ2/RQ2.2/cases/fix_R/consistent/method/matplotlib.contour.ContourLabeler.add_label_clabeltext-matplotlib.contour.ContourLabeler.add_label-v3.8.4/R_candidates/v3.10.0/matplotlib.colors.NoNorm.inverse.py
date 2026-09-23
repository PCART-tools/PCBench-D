    def inverse(self, value):
        if np.iterable(value):
            return np.ma.array(value)
        return value
