    @unpack_zerodim_and_defer("__rdivmod__")
    def __rdivmod__(self, other):
        # Note: This is a naive implementation, can likely be optimized
        if isinstance(other, (timedelta, np.timedelta64, Tick)):
            other = Timedelta(other)

        res1 = other // self
        res2 = other - res1 * self
        return res1, res2
