    def __array__(self, dtype=None) -> np.ndarray:
        # overriding DatetimelikeArray
        return np.array(list(self), dtype=object)
