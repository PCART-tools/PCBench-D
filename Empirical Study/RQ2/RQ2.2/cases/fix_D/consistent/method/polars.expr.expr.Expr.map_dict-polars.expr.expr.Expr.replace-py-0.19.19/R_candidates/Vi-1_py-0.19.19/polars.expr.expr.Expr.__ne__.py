    def __ne__(self, other: Any) -> Self:  # type: ignore[override]
        return self._from_pyexpr(self._pyexpr.neq(self._to_pyexpr(other)))
