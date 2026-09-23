    def __call__(self, value, clip=None):
        if np.iterable(value):
            return np.ma.array(value)
        return value
