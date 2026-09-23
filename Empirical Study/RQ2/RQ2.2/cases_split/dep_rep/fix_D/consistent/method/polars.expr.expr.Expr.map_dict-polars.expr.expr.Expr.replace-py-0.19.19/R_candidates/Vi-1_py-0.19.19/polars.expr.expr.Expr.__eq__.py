    def __eq__(self, other: Any) -> Self:  # type: ignore[override]
        return self._from_pyexpr(self._pyexpr.eq(self._to_pyexpr(other)))
