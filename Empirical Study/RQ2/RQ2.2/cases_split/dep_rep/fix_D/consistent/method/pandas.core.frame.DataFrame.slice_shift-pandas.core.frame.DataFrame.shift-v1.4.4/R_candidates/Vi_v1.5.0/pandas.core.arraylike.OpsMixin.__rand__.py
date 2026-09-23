    @unpack_zerodim_and_defer("__rand__")
    def __rand__(self, other):
        return self._logical_method(other, roperator.rand_)
