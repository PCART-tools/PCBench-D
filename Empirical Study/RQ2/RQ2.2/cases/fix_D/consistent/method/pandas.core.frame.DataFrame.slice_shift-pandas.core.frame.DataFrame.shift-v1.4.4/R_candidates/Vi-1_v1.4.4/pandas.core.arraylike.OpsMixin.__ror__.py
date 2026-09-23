    @unpack_zerodim_and_defer("__ror__")
    def __ror__(self, other):
        return self._logical_method(other, roperator.ror_)
