    def __pos__(self) -> SparseArray:
        return self._unary_method(operator.pos)
