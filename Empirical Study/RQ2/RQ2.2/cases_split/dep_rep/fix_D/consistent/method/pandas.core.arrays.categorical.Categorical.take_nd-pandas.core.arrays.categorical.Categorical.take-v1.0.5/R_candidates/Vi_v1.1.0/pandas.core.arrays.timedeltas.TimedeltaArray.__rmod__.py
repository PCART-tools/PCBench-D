    @unpack_zerodim_and_defer("__rmod__")
    def __rmod__(self, other):
        # Note: This is a naive implementation, can likely be optimized
        if isinstance(other, (timedelta, np.timedelta64, Tick)):
            other = Timedelta(other)
        return other - (other // self) * self
