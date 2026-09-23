    def __lt__(self, other: Any) -> Self:
        return self._from_pyexpr(self._pyexpr.lt(self._to_pyexpr(other)))
