    def __gt__(self, other: Any) -> Self:
        return self._from_pyexpr(self._pyexpr.gt(self._to_pyexpr(other)))
