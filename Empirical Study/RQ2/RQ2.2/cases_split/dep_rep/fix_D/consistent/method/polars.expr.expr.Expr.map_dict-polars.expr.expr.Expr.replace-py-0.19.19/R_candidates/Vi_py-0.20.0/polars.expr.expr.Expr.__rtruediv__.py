    def __rtruediv__(self, other: Any) -> Self:
        return self._from_pyexpr(self._to_pyexpr(other) / self._pyexpr)
