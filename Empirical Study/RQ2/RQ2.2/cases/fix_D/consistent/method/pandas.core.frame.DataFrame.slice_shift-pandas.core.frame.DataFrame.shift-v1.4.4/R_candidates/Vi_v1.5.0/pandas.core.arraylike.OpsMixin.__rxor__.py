    @unpack_zerodim_and_defer("__rxor__")
    def __rxor__(self, other):
        return self._logical_method(other, roperator.rxor)
