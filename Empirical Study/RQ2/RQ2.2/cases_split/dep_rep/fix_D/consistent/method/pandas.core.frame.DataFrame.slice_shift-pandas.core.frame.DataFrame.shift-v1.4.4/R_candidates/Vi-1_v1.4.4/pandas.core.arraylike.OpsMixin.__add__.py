    @unpack_zerodim_and_defer("__add__")
    def __add__(self, other):
        return self._arith_method(other, operator.add)
