    def __eq__(self, other: Any) -> Self:  # type: ignore[override]
        _warn_null_comparison(other)
        return self._from_pyexpr(self._pyexpr.eq(self._to_pyexpr(other)))
