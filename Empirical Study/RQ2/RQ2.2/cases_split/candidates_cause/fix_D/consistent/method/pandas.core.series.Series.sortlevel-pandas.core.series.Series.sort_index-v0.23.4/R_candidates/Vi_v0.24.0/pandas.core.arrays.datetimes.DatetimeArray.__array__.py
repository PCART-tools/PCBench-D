    def __array__(self, dtype=None):
        if dtype is None and self.tz:
            # The default for tz-aware is object, to preserve tz info
            dtype = object

        return super(DatetimeArray, self).__array__(dtype=dtype)
