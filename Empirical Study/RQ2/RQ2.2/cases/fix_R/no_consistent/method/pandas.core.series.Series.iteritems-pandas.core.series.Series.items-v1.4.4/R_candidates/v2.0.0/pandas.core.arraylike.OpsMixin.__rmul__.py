    @unpack_zerodim_and_defer("__rmul__")
    def __rmul__(self, other):
        return self._arith_method(other, roperator.rmul)
