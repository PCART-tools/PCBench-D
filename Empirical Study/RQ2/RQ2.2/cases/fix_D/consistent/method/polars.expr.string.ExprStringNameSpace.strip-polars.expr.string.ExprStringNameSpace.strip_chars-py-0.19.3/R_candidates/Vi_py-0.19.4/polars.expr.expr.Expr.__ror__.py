    def __ror__(self, other: Any) -> Self:
        return self._from_pyexpr(self._to_pyexpr(other)._or(self._pyexpr))
