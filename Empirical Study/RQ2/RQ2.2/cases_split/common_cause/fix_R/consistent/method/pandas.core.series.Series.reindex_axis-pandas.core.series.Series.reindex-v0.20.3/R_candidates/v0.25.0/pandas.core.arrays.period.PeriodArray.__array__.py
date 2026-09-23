    def __array__(self, dtype=None):
        # overriding DatetimelikeArray
        return np.array(list(self), dtype=object)
