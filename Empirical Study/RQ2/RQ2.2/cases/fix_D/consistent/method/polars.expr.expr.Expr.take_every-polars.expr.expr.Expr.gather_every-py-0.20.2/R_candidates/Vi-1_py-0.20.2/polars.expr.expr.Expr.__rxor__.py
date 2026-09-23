    def __rxor__(self, other: Any) -> Self:
        return self._from_pyexpr(self._to_pyexpr(other)._xor(self._pyexpr))
