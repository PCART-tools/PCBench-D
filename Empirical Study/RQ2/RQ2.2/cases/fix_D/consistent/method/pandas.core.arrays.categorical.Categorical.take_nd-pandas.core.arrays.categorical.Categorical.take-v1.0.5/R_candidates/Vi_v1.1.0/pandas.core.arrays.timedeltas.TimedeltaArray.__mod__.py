    @unpack_zerodim_and_defer("__mod__")
    def __mod__(self, other):
        # Note: This is a naive implementation, can likely be optimized
        if isinstance(other, (timedelta, np.timedelta64, Tick)):
            other = Timedelta(other)
        return self - (self // other) * other
