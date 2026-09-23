    def __neg__(self) -> SparseArray:
        return self._unary_method(operator.neg)
