    @unpack_zerodim_and_defer("__divmod__")
    def __divmod__(self, other):
        # Note: This is a naive implementation, can likely be optimized
        if isinstance(other, (timedelta, np.timedelta64, Tick)):
            other = Timedelta(other)

        res1 = self // other
        res2 = self - res1 * other
        return res1, res2
