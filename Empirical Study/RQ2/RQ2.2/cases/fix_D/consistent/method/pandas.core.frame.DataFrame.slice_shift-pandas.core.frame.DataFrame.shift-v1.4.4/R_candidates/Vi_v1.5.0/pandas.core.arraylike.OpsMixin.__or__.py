    @unpack_zerodim_and_defer("__or__")
    def __or__(self, other):
        return self._logical_method(other, operator.or_)
