    def __invert__(self) -> SparseArray:
        return self._unary_method(operator.invert)
