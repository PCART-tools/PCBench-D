    def __array__(self, dtype=None) -> np.ndarray:
        if dtype is None and self.tz:
            # The default for tz-aware is object, to preserve tz info
            dtype = object

        return super().__array__(dtype=dtype)
