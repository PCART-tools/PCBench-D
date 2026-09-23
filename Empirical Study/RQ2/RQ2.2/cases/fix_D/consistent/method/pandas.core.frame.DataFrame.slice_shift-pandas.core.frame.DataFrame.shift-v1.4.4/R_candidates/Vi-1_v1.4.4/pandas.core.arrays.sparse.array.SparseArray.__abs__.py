    def __abs__(self) -> SparseArray:
        return self._unary_method(operator.abs)
